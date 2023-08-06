import { StorageUtils, getProvidersFromApp } from './storage-utils';
import { uniqBy } from 'lodash';
import { INotification } from 'jupyterlab_toastify';
/**
 * Function to get the current notebook including the ipynb content
 * @param {*} args 
 * @returns current active notebook
 */
export const getCurrent = (args = null, app, notebooks) => {
    const widget = notebooks.currentWidget;
    const activate = args ? args['activate'] !== false : false;

    if (activate && widget) {
        app.shell.activateById(widget.id);
    }

    return widget;
}

export const toJSONWithDasboards = (json) => {
    return () => {
        let success = false;
        json.cells.forEach((cell) => {
            if (cell.cell_type === 'code' && cell.source) {
                const source = cell.source.split('\n');
                source.forEach(s => {
                    // Searching for a format like ".studio('My app')""
                    if (s.match(`studio\\((\\s?)+(app=)?[\\'\\"](.*?)[\\'\\"]`)) {
                        const appName = s.match(`studio\\((\\s?)+(app=)?[\\'\\"](.*?)[\\'\\"]`)[3];

                        let apps = StorageUtils.getAppsByName(appName, true);
                        apps.sort((a, b) => { return a.creationDate - b.creationDate; });
                        const appsLength = apps.length;
                        if (appsLength > 0) {
                            // Taking the latest app created
                            const app = apps[appsLength - 1];
                            const appProviders = getProvidersFromApp(app);
                            const dashboardId = app.id;

                            cell['metadata']['cf_studio_app'] = {};
                            cell['metadata']['cf_studio_providers'] = [];

                            cell['metadata']['cf_studio_app'][`cfs.app-${dashboardId}`] = app;
                            cell['metadata']['cf_studio_providers'] = uniqBy([...appProviders], 'name');

                            success = true;
                        }
                    }
                });
            }
        });

        if (success) {
            INotification.success('The cf.studio apps changes were saved into this notebook');
        }
        
        return json;
    }
};
