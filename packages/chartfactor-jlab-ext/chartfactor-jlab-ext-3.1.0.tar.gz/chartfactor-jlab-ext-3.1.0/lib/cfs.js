import { DisposableDelegate } from '@phosphor/disposable';
import { StorageUtils } from './storage-utils';
import { getCurrent } from './commons';
import { NotebookActions } from '@jupyterlab/notebook';
import { toJSONWithDasboards } from './commons';

export default class CfsExtension {
    constructor(app, notebooks) {
        this.app = app;
        this.notebooks = notebooks;        
        this.createIframe();
    }

    createIframe() {
        let iframe = document.getElementById('cfsIframe');

        if (!iframe) {
            iframe = document.createElement('iframe');
            try {
                iframe.id = 'cfsIframe';
                iframe.name = 'cfsIframe';
                iframe.src = 'https://chartfactor.com/studio/';
                iframe.style.display = 'none';  
                iframe.addEventListener("load", () => {
                    if (this.resolve) this.resolve(true);
                });          
                document.body.appendChild(iframe);
            } catch (err) {
                console.error('Oops, unable to create the Iframe element.', err);
            }
        }

        this.iframe = iframe;
    };

    async onSave(context, state) {
        const current = getCurrent(null, this.app, this.notebooks);
        if (current) {
            if (!this.toJSON) this.toJSON = current.model.toJSON;
            switch(state) {
                case 'started':                                 
                    const json = this.toJSON.call(current.model);        
                    current.model.toJSON = toJSONWithDasboards(json);
                    break;
                case 'completed':
                    current.model.toJSON = this.toJSON;
                    delete this.toJSON;
                    break;
                default:
                    break;
            }
        }
    }

    /**
     * Receive the CFS information sent from CharFactor Studio 
     * and saves or deletes it from local Jupyter Lab storage.
     * @param {} event 
     */
    cfsSynchronizeMessageEventListener(event) {
        if (event.data.action === 'synchronizeCfs') {
            if (event.data.storageItem) {
                StorageUtils.save(event.data.storageKey, event.data.storageItem);
            } else {
                // If event.data.storageItem is null then we need to remove the storageKey from local storage
                StorageUtils.remove(event.data.storageKey);
            }            
        }
    }

    /**
     * This function send the Charfactor Studio info contained in the cell's metadata
     * to chartfactor.com/studio to save it into the local storage.
     * @param {} cell 
     */
    async sendCfsInfoToStudio(cell) {
        delete this.iframeLoadedPromise;
        delete this.resolve;
        // Getting url from studio() func if defined
        const source = cell.source.split('\n');
        source.forEach(s => {
            // Searching for a format like ".studio('My app', url='http://localhost:3333')" or 
            // ".studio('My app', 'http://localhost:3333')"
            if (s.includes('cf.studio')) {
                const match = s.match(`studio\\((\\s?)+(app=)?[\\'\\"](.*)[\\'\\"]\\,(\\s?)+(url=)?[\\'\\"](.*?)[\\'\\"]\\)`);
                let iframeUrl;
                if (match) {
                    iframeUrl = match[6];
                    if (iframeUrl && iframeUrl.startsWith('http')) {
                        iframeUrl = iframeUrl.trim();
                        // Adding trailing slash if missing
                        iframeUrl = iframeUrl.replace(/\/?$/, '/');                            
                        this.iframeLoaded = $.Deferred();
                    }
                } else {
                    iframeUrl = 'https://chartfactor.com/studio/';
                }

                if (this.iframe.src !== iframeUrl) {
                    this.iframe.src = iframeUrl;
                    this.iframeLoadedPromise = new Promise((resolve, reject) => {this.resolve = resolve;});
                }
            }
        });

        if (this.iframeLoadedPromise) await this.iframeLoadedPromise    
        if (this.iframe) {
            // Synchronizing cell's app
            if (cell.metadata.cf_studio_app) {
                const keys = _.keys(cell.metadata.cf_studio_app);   
                if (keys && keys.length > 0) {
                    cell.metadata.cf_studio_app[keys[0]].creationDate = Date.now();
                    console.log('Sending the cfs info stored in the notebook to ChartFactor Studio...');
                    this.iframe.contentWindow.postMessage({
                        action: 'synchronizeCfs',
                        storageKey: keys[0],
                        storageItem: cell.metadata.cf_studio_app[keys[0]]
                    }, '*');
                }
            }

            // Synchronizing cell's providers
            if (cell.metadata.cf_studio_providers) {
                this.iframe.contentWindow.postMessage({
                    action: 'synchronizeCfs',
                    storageKey: 'cfs.dataProviders',
                    storageItem: cell.metadata.cf_studio_providers
                }, '*');
            }
        }       
    }

    createNew(panel, context) {

        /**
         * When the promise is fullfilled, then every 'code' cell is being checking 
         * in order to detect if contains any ChartFactor Studio app in the metadata,
         * and send that info to Studio to save it in the local storage.
         */
        context.ready.then(async s => {            
            try { window.removeEventListener('message', window.cfsSynchronizeMessageEventListener, false); } catch (e) { }
            window.addEventListener('message', window.cfsSynchronizeMessageEventListener = this.cfsSynchronizeMessageEventListener, false);

            const current = getCurrent(null, this.app, this.notebooks);
            const notebookConfig = current.model.toJSON(current.model);            

            // Synchronizing the apps and the providers with CF Studio
            for (const cell of notebookConfig.cells) {
                if (cell.cell_type === 'code' && cell.metadata) {
                    await this.sendCfsInfoToStudio(cell);
                }
            }           
        }).catch(e => console.error(e))

        /**
         * This event is in charge to check the current executed cell in order 
         * to detect if contains any ChartFactor Studio app in the metadata,
         * and send that info to Studio to save it in the local storage.
         */
        NotebookActions.executed.connect(async (_, args) => {
            const { cell } = args;
            
            if (cell.model.type === 'code') {
                const current = getCurrent(null, this.app, this.notebooks);
                const notebookConfig = current.model.toJSON(current.model);
                const cellId = cell.model.id;                            
                // Getting the executed cell from the notebook config
                const cellObj = notebookConfig.cells.find(c => c.id === cellId);

                if (cellObj && cellObj.metadata){
                    await this.sendCfsInfoToStudio(cellObj);
                }
            }                        
        });

        context.saveState.connect(this.onSave, this);

        return new DisposableDelegate(() => {
            return;
        });
    }
}
