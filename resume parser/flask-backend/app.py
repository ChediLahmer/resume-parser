import unicodedata
from flask import Flask, render_template, request , jsonify
import pdfplumber
import re
import pathlib
import fitz
from werkzeug.utils import secure_filename

from flask_cors import CORS

import pandas as pd
app = Flask(__name__)
CORS(app)
my_array = ["CONTACT", "WORK EXPERIENCE", "EDUCATION", "SKILLS","PROJECTS"]
roles_dataset = [
    "Web Developer",
    "Mobile Developer",
    "Data Scientist",
    "Software Engineer",
    "Network Engineer",
    "Database Administrator",
    "Cybersecurity Analyst",
    "Machine Learning Engineer",
    "Systems Analyst",
    "UI/UX Designer",

]
skills_dataset = ['assembly', 'batchfile', 'c', 'c#', 'c++', 'clojure', 'coffeescript', 'css', 'elixir', 'emacs lisp', 'go', 'haskell', 'html', 'java', 'javascript', 'jupyter notebook', 'kotlin', 'lua', 'matlab', 'objective-c', 'objective-c++', 'ocaml', 'perl', 'php', 'powershell', 'purebasic', 'python', 'rascal', 'ruby', 'rust', 'scala', 'shell', 'swift', 'tex', 'typescript', 'vim script', 'vue', '1-wire', '2d', '3d', '3d-engine', '3d-game-engine', 'accessibility', 'accordion', 'acme', 'acme-client', 'activejob', 'activerecord', 'activity', 'activity-stream', 'actor-model', 'adc', 'addons', 'admin', 'admin-dashboard', 'admin-template', 'admin-theme', 'admin-ui', 'ado-net', 'adobe', 'after-effects', 'ag', 'agc', 'agent', 'airbnb', 'airtable', 'akka', 'alarm', 'alerting', 'algorithm', 'algorithm-challenges', 'algorithm-competitions', 'alignment', 'amd', 'analytics', 'android', 'android-application', 'android-architecture', 'android-cleanarchitecture', 'android-development', 'android-interview-questions', 'android-library', 'android-testing', 'android-ui', 'angular', 'angular-2', 'angular-components', 'angular2', 'angular4', 'angularclass', 'angularjs', 'angularjs-interview-questions', 'animation', 'animation-library', 'anonymity', 'ansible', 'antd', 'anticensorship', 'anyconnect', 'aot', 'aot-compilation', 'apache', 'api', 'api-documentation', 'api-gateway', 'api-management', 'apis', 'apollo', 'app', 'apple', 'apple-swift', 'apple-tv', 'apple-watch', 'apps', 'arbre', 'architectural', 'arduino', 'arrow-functions', 'artificial-intelligence', 'asp', 'assert', 'assertion-library', 'assertions', 'ast', 'async', 'async-functions', 'asynchronous', 'asyncio', 'athena', 'atom', 'audio', 'audio-library', 'audit', 'aurelia-framework', 'authentication', 'auto', 'autocomplete', 'autolayout', 'automatic-https', 'automation', 'awesome', 'awesome-list', 'awesome-lists', 'awesomeness', 'aws', 'aws-lambda', 'aws-s3', 'azure-functions', 'babel', 'backbone', 'backbone-framework', 'bar', 'barcode', 'barcode-scanner', 'bash', 'bayesian-methods', 'bdd', 'beaglebone-black', 'bem', 'benchmark', 'best-performance', 'best-practices', 'bi', 'big-data', 'bigquery', 'binaries', 'bioinformatics', 'bitcoin', 'bittorrent', 'blade', 'blog', 'blog-engine', 'blogging', 'bluetooth', 'bodymovin', 'boilerplate', 'book', 'book-series', 'books', 'bootstrap', 'bootstrap4', 'bot', 'bot-application', 'botkit-bots', 'botkit-studio', 'bots', 'bottom-navigation', 'bourbon-family', 'brew', 'browser', 'browser-extension', 'browsersync', 'bug-bounty', 'build', 'build-automation', 'build-pipelines', 'build-system', 'build-tool', 'build-tools', 'bundle', 'burger-menu', 'business', 'button', 'c-plus-plus', 'c-plus-plus-11', 'c-sharp', 'c89', 'cache', 'cachet', 'caddyfile', 'caffe', 'calendar', 'callbacks', 'canvas', 'canvas2d', 'card', 'careers', 'carousel', 'carthage', 'certificate', 'certification', 'chai', 'chart', 'charting-library', 'chat', 'cheatsheets', 'chip', 'chrome', 'chrome-browser', 'cisco-spark', 'clean-architecture', 'cli', 'cli-app', 'cli-dashboard', 'client', 'client-side', 'clojure-development', 'clojurescript', 'closures', 'cloud', 'cloud-management', 'cloud-native', 'cloud-providers', 'cloud-provisioning', 'cloud-storage', 'cluster', 'cms', 'cncf', 'cockroachdb', 'cocoa', 'cocoapods', 'cocos2d-html5', 'cocos2d-js', 'code', 'code-analysis', 'code-examples', 'code-quality', 'codehub', 'codepath', 'coding', 'coding-challenge', 'coding-challenges', 'coding-interview', 'coding-interviews', 'collaboration', 'collection', 'collections', 'color-scheme', 'command-line', 'command-line-tool', 'commerce-engine', 'commonjs', 'community', 'community-driven', 'competitive-programming', 'compiler', 'component', 'components', 'composer', 'composition', 'computer-architecture', 'computer-science', 'computer-vision', 'concurrency', 'configuration', 'configuration-management', 'consensus', 'console', 'constraint-programming', 'constraints', 'consul', 'container', 'containers', 'content', 'content-management', 'content-management-system', 'contentprovider', 'continuous-delivery', 'continuous-integration', 'convert', 'cordova', 'coreclr', 'correct', 'cosmicmind', 'couchdb', 'counter', 'courses', 'coverage', 'cpp', 'cpp-library', 'cppcon', 'crash-reporting', 'crash-reports', 'crawler', 'creative', 'credit-card', 'cross-browser', 'cross-platform', 'cryptocurrency', 'cryptography', 'csharp', 'csp-report', 'css-animations', 'css-effects', 'css-framework', 'css-in-js', 'css-skills', 'css3', 'css3-features', 'curated', 'curl', 'custom-elements', 'custom-transitions', 'customtags', 'd3', 'dac', 'dagger2', 'dagger2-mvp', 'dapper', 'dash', 'dashboard', 'dashboards', 'data', 'data-analysis', 'data-binding', 'data-grid', 'data-mining', 'data-science', 'data-structure', 'data-visualization', 'database', 'databases', 'databinding', 'date', 'datepicker', 'daterange', 'daterangepicker', 'datetime-picker', 'debugging', 'decentralized', 'deep-io', 'deep-learning', 'deep-neural-networks', 'deeplearning', 'dependency-manager', 'deploy', 'deployment', 'deserialization', 'design', 'design-pattern', 'design-patterns', 'design-system', 'design-systems', 'design-thinking', 'designpatternsphp', 'desktop', 'desktop-app', 'desktop-application', 'detection', 'dev-ops', 'devarchy', 'developer', 'developer-tools', 'development', 'device-detection', 'devops', 'devtools', 'dialog', 'diff', 'diff-highlight', 'disk-encryption', 'distributed', 'distributed-actors', 'distributed-computing', 'distributed-database', 'distributed-systems', 'distributed-transactions', 'diy', 'django', 'dl4j', 'docker', 'docker-compose', 'docker-image', 'dockerfile', 'docs', 'doctrine', 'documentation', 'documentation-tool', 'dom', 'dotnet', 'dotnet-core', 'dotnetcore', 'drag', 'drag-and-drop', 'drag-drop', 'draggable', 'dragging', 'drawer', 'drawer-support', 'drawerlayout', 'dropdown', 'droppable', 'dropzone', 'druid', 'dsl', 'dts', 'dx', 'dynamic', 'dynamic-table', 'e-commerce', 'easing-functions', 'easy', 'easy-to-use', 'echo', 'ecmascript', 'ecommerce-platform', 'editor', 'education', 'effects', 'efficiency', 'elasticsearch', 'electron', 'electron-app', 'elegant', 'email', 'email-sender', 'emberjs', 'encode', 'encrypt', 'end-to-end', 'enterprise', 'erp', 'error-log', 'error-monitoring', 'es2015', 'es6', 'es6-javascript', 'eslint', 'esm', 'etcd', 'etl-framework', 'event-management', 'event-stream', 'example', 'examples', 'exoplayer', 'expectation', 'exploitation', 'express', 'extensible', 'extension', 'face-recognition', 'facebook', 'facenet', 'fake', 'fake-content', 'fake-data', 'faker-generator', 'fast', 'feathersjs', 'feature-detection', 'federated', 'fetch', 'ffmpeg', 'file', 'file-upload', 'files', 'fineuploader', 'fish', 'flash', 'flat-file', 'flavor', 'flavortown', 'flexbox', 'flexible', 'flow', 'flux', 'font', 'font-face', 'forever', 'forhumans', 'form', 'form-builder', 'form-validation', 'forms', 'foss', 'fragment', 'framework', 'free', 'freebsd', 'front-end', 'front-end-framework', 'frontend', 'fullpage', 'fullscreen', 'functional', 'functional-programming', 'fuzz-testing', 'fuzzing', 'fuzzy-search', 'fzf', 'gallery', 'game', 'game-development', 'game-engine', 'game-frameworks', 'gamedev', 'gang-of-four', 'gbdt', 'gbm', 'gbrt', 'generator', 'gfw', 'git', 'github-api', 'glsl', 'gnu-social', 'goagent', 'godotengine', 'gogs', 'golang', 'golang-library', 'good-practices', 'google', 'google-cloud-functions', 'google-material', 'gpio', 'gpu', 'gradle-plugin', 'graph', 'graphics', 'graphite', 'graphql', 'grav', 'grid-editor', 'growth', 'gui', 'guide', 'guidelines', 'guides', 'hack', 'hacking', 'hacklang', 'hacks', 'hadoop', 'hashchange', 'head', 'headless-browsers', 'headless-chrome', 'headless-testing', 'health-check', 'help', 'heroku', 'hexo', 'hg', 'hhvm', 'high-performance', 'hls', 'hmr', 'home-automation', 'homebrew', 'hosting', 'hotfix', 'htaccess-snippets', 'html-template', 'html5', 'html5-audio', 'html5-charts', 'html5-game-development', 'html5-history', 'html5-history-api', 'html5-video', 'http-client', 'http-server', 'http2', 'httpclient', 'hud', 'hugo', 'hyperscript', 'hyperterm', 'i18n', 'i2c', 'ibm-openwhisk', 'icons', 'ide', 'image', 'image-processing', 'imageview', 'imgui', 'immersive', 'immutablejs', 'indexeddb', 'inferno-component', 'inferno-js', 'influxdb', 'infrastructure-as-code', 'infrastructure-management', 'inheritance', 'inline-validation', 'input', 'input-mask', 'intel', 'intellij', 'intellij-plugin', 'interactive-visualizations', 'internet-freedom', 'internet-of-things', 'interview', 'interview-practice', 'interview-prep', 'interview-preparation', 'interview-questions', 'interviewing', 'intranet', 'introjs', 'intrusion-detection', 'io', 'ionic', 'ios', 'ios-animation', 'ios-app', 'ios-transition', 'ios-ui', 'iot', 'ipad', 'ipfs', 'iphone', 'ipld', 'ipsec', 'ipython', 'ipython-notebook', 'iqkeyboardmanager', 'iris', 'isolation', 'isomorphic-javascript', 'istanbul', 'jasmine', 'java-8', 'javascript-compiler', 'javascript-interview-questions', 'javascript-library', 'javascript-modules', 'javascript-tips', 'jekyll-site', 'jest', 'jinja', 'jobs', 'journalism', 'jpeg-encoder', 'jquery', 'jruby', 'js', 'jsbridge', 'json', 'json-logging', 'json-parser', 'json-serialization', 'json-serializer', 'jspatch', 'jsqmessagesviewcontroller', 'jss', 'jsx', 'julia-language', 'jupyter', 'jupyter-notebook', 'jvm-languages', 'kaggle', 'karma', 'kennethreitz', 'keras', 'key-value', 'keyboard', 'keyboard-shortcuts', 'keyframes', 'kingfisher', 'knowledge', 'koa', 'kotlin-library', 'kubernetes', 'l2tp', 'labstack-echo', 'lambda-expressions', 'language', 'laravel', 'layout', 'lazy-evaluation', 'lazy-loading', 'lazyload', 'leaflet', 'learn-to-code', 'learning-by-doing', 'leetcode', 'leetcode-java', 'leetcode-questions', 'leetcode-solutions', 'less', 'letsencrypt', 'libraries', 'library', 'lighttable', 'links', 'lint', 'lint-checking', 'linter', 'linters', 'linting', 'linux', 'linux-kernel', 'list', 'lists', 'lite', 'load-balancer', 'loaders', 'localforage', 'localstorage', 'log', 'logcat', 'logging', 'logistic-regression', 'lottie', 'lstm', 'luajit', 'mac', 'mac-osx', 'machine-learning', 'machine-learning-algorithms', 'macos', 'macos-setup', 'macosx', 'mail', 'mail-server', 'man-in-the-middle', 'man-page', 'management', 'manager', 'manpages', 'manual', 'mapreduce', 'maps', 'marathon', 'marionettejs', 'markdown', 'marketing', 'marshalling', 'material', 'material-colors', 'material-components', 'material-design', 'material-theme', 'material-ui', 'materialdrawer', 'math', 'mathematical-analysis', 'matplotlib', 'maven-plugin', 'mediaplayer', 'memoized-selectors', 'menu-navigation', 'menubar', 'mesos', 'message', 'message-queue', 'messaging', 'messenger', 'meta-tags', 'metallica', 'meteor', 'metrics', 'micro-framework', 'microkernel', 'microservice', 'microservices', 'microsoft', 'microsoft-bot-framework', 'middleware', 'mikepenz', 'mindmaps', 'minification', 'minimal', 'mit', 'ml', 'mobile', 'mobile-database', 'mobile-detect', 'mobile-web', 'mobx', 'mocha', 'mochajs', 'mocking', 'mocks', 'modal', 'models', 'modern-php', 'modernizr', 'module-bundler', 'module-loader', 'modules', 'mongodb', 'monitoring', 'motion', 'motion-graphics', 'mousewheel', 'mozilla', 'mpv', 'mqtt', 'multi-platform', 'multiformats', 'mvc', 'mvc-framework', 'mvp', 'mvp-android', 'mvvm-architecture', 'mysql', 'named-entity-recognition', 'naming-conventions', 'nasa', 'natural-language-processing', 'navigation-controller', 'navigation-drawer', 'neovim', 'netcore', 'network', 'networking', 'neural-nets', 'neural-network', 'neural-networks', 'newsql', 'nextjs', 'ng2', 'nginx', 'nlp', 'node', 'node-webkit', 'nodebb', 'nodejs', 'nodemon', 'normalize', 'nosql-database', 'notebook', 'notifications', 'npm', 'nsq', 'numpy', 'nvim', 'nwjs', 'oauth2', 'objc-runtime', 'object-oriented', 'object-storage', 'objective-c-extensions', 'objective-c-library', 'observer', 'oci', 'ocr', 'ocr-engine', 'odoo', 'odoo-apps', 'offcanvas', 'offline', 'onepage', 'oop', 'open-source', 'open-source-project', 'openapi-specification', 'openconnect', 'opentype-fonts', 'openvpn', 'operating-system', 'optimization', 'orchestration', 'orchestration-framework', 'orm', 'osx', 'otf', 'otf-fonts', 'oxford', 'p2p', 'paas', 'package-manager', 'packages', 'pagination', 'painless', 'painless-javascript-testing', 'pandas', 'parallel-streams', 'parser', 'part-of-speech', 'payments', 'pcduino', 'pcre', 'pdf', 'peer-to-peer', 'penetration-testing', 'pentesting', 'pentesting-windows', 'perfect', 'performance', 'performance-analysis', 'performance-metrics', 'permission', 'phantomjs', 'phaserjs', 'phone', 'phonegap', 'photon', 'photos', 'php-applications', 'php-extension', 'php-framework', 'php-installation', 'php-library', 'php7', 'phpunit', 'picker', 'pixi', 'pixijs', 'plataformatec', 'play', 'playback', 'player', 'playground', 'plugins', 'plyr', 'pm2', 'pods', 'polyfill', 'popover', 'popup', 'postcss-plugins', 'postgresql', 'preact-components', 'preprocessor', 'presentations', 'pretty-printer', 'principles', 'printer', 'privacy', 'procedural-generation', 'process', 'process-manager', 'production', 'productivity', 'programmer', 'programming', 'programming-blogs', 'programming-language', 'programming-ligatures', 'programming-tutorial', 'progress', 'progressive-web-app', 'prometheus', 'promise', 'prompt', 'protobuf-runtime', 'protoc', 'protocol-buffers', 'protocol-compiler', 'prototypes', 'protractor', 'proxy', 'psr-11', 'psr-13', 'psr-16', 'psr-3', 'psr-6', 'psr-7', 'pty', 'pure', 'purecss', 'purelayout', 'pwa', 'pwm', 'pymc', 'python-interview-questions', 'qa', 'queue', 'qunit', 'rack', 'raft', 'rails', 'rails-helper', 'rails-interview', 'rapid-development', 'raspberry-pi', 'react', 'react-components', 'react-native', 'react-renderer', 'react-router', 'reactive', 'reactive-programming', 'reactive-streams', 'reactivecocoa', 'reactiveswift', 'reactivex', 'reactjs', 'real-time', 'real-time-processing', 'realtime', 'realtime-database', 'recyclerview-adapter', 'recyclerview-item-animation', 'redis', 'redshift', 'redux', 'redux-documentation', 'redux-saga', 'reference', 'regex', 'remote-execution', 'renderer', 'rendering', 'rendering-2d-graphics', 'rendering-engine', 'reordering', 'repl', 'requests', 'research', 'resource', 'resources', 'responsive', 'responsive-images', 'rest', 'rest-api', 'restful', 'restful-api', 'reveal', 'reverse-engineering', 'reverse-proxy', 'rfc822', 'rich-text-editor', 'rkt', 'robotics', 'router', 'routing', 'rpc', 'rpc-framework', 'ruby-language', 'rubyonrails', 'runtime', 'rxjava', 'rxjava-android', 'rxjs', 'rxswift', 's3-storage', 'saas', 'sagas', 'sage', 'sandstorm', 'sanitization', 'sass', 'sass-functions', 'sass-library', 'sass-mixins', 'scaffolding', 'scala-compiler', 'scala-library', 'scala-programming-language', 'scalable', 'scale', 'scene-graph', 'scheduling', 'scientific-computing', 'scikit-learn', 'scipy', 'screenshots', 'scripting', 'scroll', 'scrolling', 'scss', 'sdk', 'search', 'search-engine', 'search-in-text', 'searchbar', 'sections', 'security', 'security-book', 'security-checklist', 'select', 'selenium', 'selenium-webdriver', 'self-hosted', 'semantic', 'semantic-engine', 'serial', 'serialization', 'server', 'server-rendering', 'server-side-rendering', 'server-side-swift', 'serverless', 'serverless-architectures', 'serverless-framework', 'service-consumer', 'service-discovery', 'service-mesh', 'service-oriented', 'service-provider', 'service-registration', 'service-registry', 'shadowsocks', 'sidebar', 'signalr', 'silver-searcher', 'simple', 'simple-api', 'single-header-lib', 'single-page-applications', 'sinon', 'sites', 'sketch', 'sketch-plugin', 'slack', 'slate', 'slide', 'slideout-menu', 'slides', 'slideshow', 'smtp', 'snackbar', 'snap', 'snapkit', 'snapshot', 'snippets', 'soa', 'social-network', 'socket-communication', 'socket-io', 'software', 'software-development', 'sort', 'sortable', 'spa', 'spacegray-eighties', 'spacegray-light', 'spannable-string', 'spark', 'spi', 'spreadsheet', 'spring', 'spring-boot', 'sprites', 'sql', 'sql-editor', 'sql-injection', 'ssh', 'sshuttle', 'ssl', 'ssr', 'stack', 'standalone', 'standard', 'starter-kit', 'startup-script', 'state-machine', 'state-management', 'state-tree', 'static-analysis', 'static-code-analysis', 'static-site-generator', 'statistics', 'statsd', 'status', 'statuspage', 'storage', 'store-json', 'storefront', 'str8c', 'stream', 'streaming', 'stunnel', 'style-guide', 'style-linter', 'styled-components', 'styleguide', 'stylesheets', 'sublime-text', 'super-resolution', 'svg', 'svg-animations', 'svgo', 'svn', 'svprogresshud', 'swagger-api', 'swagger-js', 'swift-3', 'swift-extensions', 'swift-framework', 'swift-language', 'swift-library', 'swift-perfect-community', 'swift-programming', 'swift-wrapper', 'swift3', 'swiftyjson', 'swipe', 'swiper', 'symfony', 'symfony-bundle', 'sync', 'synchronization', 'syntax-checker', 'syntax-checking', 'syntax-highlighting', 'system', 'systems', 'tabbarcontroller', 'tabbaritem', 'tagging', 'tap', 'tdd', 'teachers', 'tech', 'technical-coding-interview', 'templates', 'tensorflow', 'terminal', 'terminal-emulators', 'tessel', 'tesseract', 'tesseract-ocr', 'test', 'test-framework', 'test-runner', 'test-runners', 'testing', 'testing-tools', 'text-editor', 'textfield', 'theano', 'theme', 'threadsafe', 'tidb', 'timber', 'time', 'time-series', 'time-travel', 'tips', 'tips-and-tricks', 'tldr', 'tldr-pages', 'tls', 'tmux', 'toast', 'toolbox', 'tools', 'tooltip', 'tooltip-library', 'tor', 'torch', 'torrent', 'touch', 'touch-events', 'tour', 'tox', 'training-materials', 'training-providers', 'transition-animation', 'translation', 'traversal', 'treeview', 'tricks', 'ttf', 'tty', 'tutorial', 'tutorials', 'tvos', 'twig', 'twilio', 'typechecker', 'typeface', 'typefaces', 'types', 'typescript-definitions', 'typings', 'ui', 'ui-components', 'ui-design', 'ui-kit', 'ui-theme', 'uikit', 'uitabbarcontroller', 'unicorns', 'unidirectional', 'unit-testing', 'universal', 'universal-javascript', 'unix', 'usability', 'user-experience', 'utilities', 'ux', 'v8', 'validation', 'vanilla', 'vanilla-javascript', 'vanilla-js', 'vdom', 'vector', 'velociraptors', 'video', 'video-player', 'videojs', 'videos', 'view', 'viewcontroller', 'views', 'vim', 'vim-plugin', 'vim-plugins', 'vim-scripts', 'vimeo', 'viml', 'virtual-dom', 'visual-basic', 'visual-studio', 'visual-studio-code', 'visualization', 'visualizations', 'volume', 'vpn', 'vue-components', 'vue2', 'vuex', 'vulnerability-scanner', 'vux', 'watch', 'weapp-demo', 'web', 'web-analytics', 'web-app', 'web-application', 'web-application-framework', 'web-audio', 'web-components', 'web-development', 'web-framework', 'web-performance', 'web-server', 'web-wechat', 'webapp', 'webcomponents', 'webdriver', 'webfinger', 'webgl', 'webpack', 'webpack2', 'webplatform', 'webrtc', 'webservices', 'website', 'website-builder', 'website-generation', 'websocket', 'websocket-server', 'websockets', 'websql', 'wechat', 'weex', 'werkzeug', 'weui', 'wfc', 'wget', 'widget', 'windows', 'wireguard', 'wordpress', 'wordpress-starter-theme', 'wordpress-theme', 'wsgi', 'wxapp', 'wysiwyg', 'wysiwyg-editor', 'xcode', 'xcode-plugin', 'xhr', 'xx-net', 'yaml', 'yarn', 'yeoman-generator', 'yii', 'yii2', 'youtube', 'zephir', 'zero-configuration', 'zeromq', 'zookeeper', 'zsh', 'zsh-configuration']

majors_dataset = [
    'GENERAL AGRICULTURE',
    'AGRICULTURE PRODUCTION AND MANAGEMENT',
    'AGRICULTURAL ECONOMICS',
    'ANIMAL SCIENCES',
    'FOOD SCIENCE',
    'PLANT SCIENCE AND AGRONOMY',
    'SOIL SCIENCE',
    'MISCELLANEOUS AGRICULTURE',
    'FORESTRY',
    'NATURAL RESOURCES MANAGEMENT',
    'FINE ARTS',
    'DRAMA AND THEATER ARTS',
    'MUSIC',
    'VISUAL AND PERFORMING ARTS',
    'COMMERCIAL ART AND GRAPHIC DESIGN',
    'FILM VIDEO AND PHOTOGRAPHIC ARTS',
    'STUDIO ARTS',
    'MISCELLANEOUS FINE ARTS',
    'ENVIRONMENTAL SCIENCE',
    'BIOLOGY',
    'BIOCHEMICAL SCIENCES',
    'BOTANY',
    'MOLECULAR BIOLOGY',
    'ECOLOGY',
    'GENETICS',
    'MICROBIOLOGY',
    'PHARMACOLOGY',
    'PHYSIOLOGY',
    'ZOOLOGY',
    'NEUROSCIENCE',
    'MISCELLANEOUS BIOLOGY',
    'COGNITIVE SCIENCE AND BIOPSYCHOLOGY',
    'GENERAL BUSINESS',
    'ACCOUNTING',
    'ACTUARIAL SCIENCE',
    'BUSINESS MANAGEMENT AND ADMINISTRATION',
    'OPERATIONS LOGISTICS AND E-COMMERCE',
    'BUSINESS ECONOMICS',
    'MARKETING AND MARKETING RESEARCH',
    'FINANCE',
    'HUMAN RESOURCES AND PERSONNEL MANAGEMENT',
    'INTERNATIONAL BUSINESS',
    'HOSPITALITY MANAGEMENT',
    'MANAGEMENT INFORMATION SYSTEMS AND STATISTICS',
    'MISCELLANEOUS BUSINESS & MEDICAL ADMINISTRATION',
    'COMMUNICATIONS',

    'MASS MEDIA',
    'ADVERTISING AND PUBLIC RELATIONS',
    'COMMUNICATION TECHNOLOGIES',
    'COMPUTER AND INFORMATION SYSTEMS',
    'COMPUTER PROGRAMMING AND DATA PROCESSING',
    'COMPUTER SCIENCE',
    'INFORMATION SCIENCES',
    'COMPUTER ADMINISTRATION MANAGEMENT AND SECURITY',
    'COMPUTER NETWORKING AND TELECOMMUNICATIONS',
    'MATHEMATICS',
    'APPLIED MATHEMATICS',
    'STATISTICS AND DECISION SCIENCE',
    'MATHEMATICS AND COMPUTER SCIENCE',
    'GENERAL EDUCATION',
    'EDUCATIONAL ADMINISTRATION AND SUPERVISION',
    'SCHOOL STUDENT COUNSELING',
    'ELEMENTARY EDUCATION',
    'MATHEMATICS TEACHER EDUCATION',
    'PHYSICAL AND HEALTH EDUCATION TEACHING',
    'EARLY CHILDHOOD EDUCATION',
    'SCIENCE AND COMPUTER TEACHER EDUCATION',
    'SECONDARY TEACHER EDUCATION',
    'SPECIAL NEEDS EDUCATION',
    'SOCIAL SCIENCE OR HISTORY TEACHER EDUCATION',
    'TEACHER EDUCATION: MULTIPLE LEVELS',
    'LANGUAGE AND DRAMA EDUCATION',
    'ART AND MUSIC EDUCATION',
    'MISCELLANEOUS EDUCATION',
    'LIBRARY SCIENCE',
    'ARCHITECTURE',
    'GENERAL ENGINEERING',
    'AEROSPACE ENGINEERING',
    'BIOLOGICAL ENGINEERING',
    'ARCHITECTURAL ENGINEERING',
    'BIOMEDICAL ENGINEERING',
    'CHEMICAL ENGINEERING',
    'CIVIL ENGINEERING',
    'COMPUTER ENGINEERING',
    'ELECTRICAL ENGINEERING',
    'ENGINEERING MECHANICS PHYSICS AND SCIENCE',
    'ENVIRONMENTAL ENGINEERING',
    'GEOLOGICAL AND GEOPHYSICAL ENGINEERING',
    'INDUSTRIAL AND MANUFACTURING ENGINEERING',
    'MATERIALS ENGINEERING AND MATERIALS SCIENCE',
    'MECHANICAL ENGINEERING',
    'METALLURGICAL ENGINEERING',
    'MINING AND MINERAL ENGINEERING',
    'NAVAL ARCHITECTURE AND MARINE ENGINEERING',
    'NUCLEAR ENGINEERING',
    'PETROLEUM ENGINEERING',
    'MISCELLANEOUS ENGINEERING',
    'ENGINEERING TECHNOLOGIES',
    'ENGINEERING AND INDUSTRIAL MANAGEMENT',
    'ELECTRICAL ENGINEERING TECHNOLOGY',
    'JOURNALISM'
]


def extract_text_from_pdf(fname):
    with fitz.open(fname) as doc:
        # Extract text from each page
        text_pages = [page.get_text() for page in doc]

    # Concatenate text from all pages into a single string
    all_text = '\n'.join(text_pages)

    # Save the concatenated text to a file
    concatenated_filename = f"{fname}_concatenated.txt"
    pathlib.Path(concatenated_filename).write_text(all_text, encoding='utf-8')

    return all_text



def extract_major(text, majors_dataset, my_array):
    education_index = text.lower().find('education')
    if education_index != -1:
        for major in majors_dataset:
            if any(substring.lower() in major.lower() for substring in my_array):
                continue

            if major.lower() in text[education_index + len('education'):].lower():
                return major
    return None




def normalize_text(text):
    normalized_text = unicodedata.normalize('NFKD', text)
    return normalized_text

def extract_name(text):
    newline_index = text.find('\n')
    extracted_text = text[:newline_index].strip() if newline_index != -1 else text.strip()
    return normalize_text(extracted_text)

def extract_role(text, roles_dataset):
    for role in roles_dataset:
        if role.lower() in text.lower():
            return role

    return None


def extract_mail(text, my_array):
    contact_index = text.lower().find('contact')
    if contact_index != -1:
        for word in text[contact_index + len('contact'):].split():
            if any(substring.lower() in word.lower() for substring in my_array):
                continue
            if '@' in word and '.' in word:
                return word

    return None


def extract_experience_information(text):
    # Create a pattern to find the experience section and extract roles and associated companies
    experience_pattern = re.compile(r'\bWORK EXPERIENCE\b(.*?)(?=\bPROJECTS\b|\Z)', re.IGNORECASE | re.DOTALL)

    # Search for the experience pattern in the text
    experience_match = experience_pattern.search(text)

    if experience_match:
        # Extract the experience information from the matched group
        experience_info = experience_match.group(1)

        # Create a pattern to extract roles and associated companies
        role_and_company_pattern = re.compile(
            r'(?P<role>.*?)\n(?:\u00B7|•)?\s*(?P<company>.*?)\n(?:\u00B7|•)?\s*(?P<date>.*?)\n', re.IGNORECASE | re.DOTALL
        )

        # Find all matches of roles and associated companies in the extracted experience information
        role_and_company_matches = role_and_company_pattern.findall(experience_info)

        # Return the extracted information, roles, and associated companies
        return experience_info.strip()
    else:
        # Return default values when no experience information is found
        return '', []
def extract_projects(text, my_array):
    project_pattern = re.compile(r'\nprojects?\n(.*?)(?=\n\S|$)', re.IGNORECASE | re.DOTALL)
    project_match = project_pattern.search(text)

    if project_match:
        project_text = project_match.group(1).strip()
        if my_array:
            array_string = my_array[len(project_text) % len(my_array)]
            result = f"{project_text} {array_string}"
            return result.strip()

    return None


@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['pdfFile']

    if uploaded_file.filename != '':
        fname = 'C:/Users/fahdl/OneDrive/Desktop/files/' + secure_filename(uploaded_file.filename)
        uploaded_file.save(fname)
        mytext = extract_text_from_pdf(fname)
        myname = extract_name(mytext)
        role = extract_role(mytext, roles_dataset)
        major = extract_major(mytext, majors_dataset, my_array)
        mail = extract_mail(mytext, my_array)
        experience = extract_experience_information(mytext)
        project = extract_projects(mytext, my_array)
        resume_data = {
            'name': myname,
            'role': role,
            'major': major,
            'mail': mail,
            'projects': project,
            'experience': experience
        }
        return jsonify(resume_data)
    else:
        return 'No file selected'





if __name__ == '__main__':
    app.run(debug=True, port=5000)

