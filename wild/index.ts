import { createBackendModule } from '@backstage/backend-plugin-api';
import { scaffolderActionsExtensionPoint } from '@backstage/plugin-scaffolder-node/alpha';
import { createCustomFileAction } from './actions/custom';

const customScaffolderModule = createBackendModule({
  pluginId: 'scaffolder',
  moduleId: 'custom-action-module',
  register(env) {
    env.registerInit({
      deps: {
        scaffolder: scaffolderActionsExtensionPoint,
      },
      async init({ scaffolder }) {
        scaffolder.addActions(createCustomFileAction());
      },
    });
  },
});

// Add to your backend instance:
backend.add(customScaffolderModule);
