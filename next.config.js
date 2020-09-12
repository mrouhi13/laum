module.exports = {
  serverRuntimeConfig: {
    staticFolder: '/public',
    app: {
      domain: process.env.APP_DOMAIN,
      title: process.env.APP_TITLE,
      logo: '/images/logo.svg',
      hashtags: {
        en: [],
        fa: []
      },
      links: {
        about: process.env.APP_ABOUT_URL_ABOUT,
        contactEmail: `mailto:${process.env.APP_CONTACT_EMAIL}`,
        twitter: `https://twitter.com/${process.env.TWITTER_ACCOUNT}`,
        github: `https://github.com/${process.env.GITHUB_REPO}`
      }
    },
    firebase: {
      apiKey: process.env.FIREBASE_API_KEY,
      authDomain: process.env.FIRBASE_AUTH_DOMAIN,
      databaseURL: process.env.FIRBASE_DATABASE_URL,
      projectId: process.env.FIRBASE_PROJECT_ID,
      storageBucket: process.env.FIRBASE_STORAGE_BUCKET,
      messagingSenderId: process.env.FIRBASE_MESSAGING_SENDER_ID,
      appId: process.env.FIREBASE_APP_ID,
      measurementId: process.env.FIREBASE_MEASUREMENT_ID
    }
  },
  pageExtensions: ['jsx', 'js', 'ts', 'tsx'],
  reactStrictMode: true,
  poweredByHeader: false,
  generateEtags: false
}
