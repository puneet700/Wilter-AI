// packages/backend/src/actions/custom.ts
import { createTemplateAction } from '@backstage/plugin-scaffolder-node';
import fs from 'fs-extra';
import path from 'path';

export const createCustomFileAction = () => {
  return createTemplateAction<{ filename: string; content?: string }>({
    id: 'my:custom:action',
    description: 'Creates a new file in the workspace directory',
    schema: {
      input: {
        type: 'object',
        required: ['filename'],
        properties: {
          filename: {
            title: 'File Name',
            description: 'The name of the file to create',
            type: 'string',
          },
          content: {
            title: 'Content',
            description: 'Text content to write into the file',
            type: 'string',
          },
        },
      },
    },
    async handler(ctx) {
      const targetPath = path.join(ctx.workspacePath, ctx.input.filename);
      ctx.logger.info(`Creating file at: ${targetPath}`);

      await fs.outputFile(targetPath, ctx.input.content || 'Hello from custom action!\n');
    },
  });
};
