module.exports = {
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint/eslint-plugin'],
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:@typescript-eslint/eslint-recommended',
    'plugin:@typescript-eslint/recommended',
    'prettier',
    'prettier/@typescript-eslint'
  ],
  env: {
    es6: true,
    browser: true,
    node: true
  },
  parserOptions: {
    project: 'tsconfig.json',
    createDefaultProgram: true,
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true
    }
  },
  settings: {
    react: {
      version: 'detect'
    }
  },
  rules: {
    '@typescript-eslint/interface-name-prefix': 'on',
    '@typescript-eslint/no-explicit-any': 'warn',
    '@typescript-eslint/prefer-namespace-keyword': 'off',
    '@typescript-eslint/explicit-function-return-type': 'warn',
    '@typescript-eslint/explicit-module-boundary-types': 'off',
    '@typescript-eslint/no-empty-function': 'warn',
    '@typescript-eslint/array-type': 'warn',
    '@typescript-eslint/type-annotation-spacing': 'warn',
    '@typescript-eslint/brace-style': 'warn',
    '@typescript-eslint/comma-spacing': 'warn',
    '@typescript-eslint/dot-notation': 'warn',
    '@typescript-eslint/indent': ['warn', 4],
    '@typescript-eslint/keyword-spacing': 'warn',
    '@typescript-eslint/lines-between-class-members': 'warn',
    '@typescript-eslint/quotes': ['warn', 'single'],
    '@typescript-eslint/semi': 'off',
    'indent': 'warn',
    'default-case': 'error',
    'no-alert': 'error',
    'linebreak-style': ['error', 'unix'],
    'quotes': ['warn', 'single'],
    'no-unused-vars': [
      'warn',
      {
        'vars': 'all',
        'args': 'after-used',
        'ignoreRestSiblings': 'off',
        'argsIgnorePattern': '^_'
      }
    ],
    'react/react-in-jsx-scope': 'off',
    'react/display-name': 'on',
    'react/prop-types': 'on',
    '@typescript-eslint/explicit-member-accessibility': 'on',
    '@typescript-eslint/member-delimiter-style': 'on',
    '@typescript-eslint/no-var-requires': 'on',
    '@typescript-eslint/no-use-before-define': 'on',
    'no-console': [
      'warn',
      {
        'allow': ['warn', 'error']
      }
    ]
  }
}
