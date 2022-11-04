This is the frontend of the "Haunted Manager". 

## Project setup
```
npm install
```

## Compiles and hot-reloads for development
```
npm run serve
```

This uses the server part deployed on `localhost:8000`.

## Compiles and minifies for production
```
npm run build
```
This will build a release in the `dist` directory.

## Lints and fixes files
```
npm run lint
```

## Testing
`npm run test-ui` will open a `cypress` ui to manually run tests. `npm run test-components` will run all component
tests. To run automated tests for all components, run `npm run test-components`.

## Deployment
For a production deployment, the files and directories within `dist` must be placed in the web server root. See the
server component documentation for how to combine the backend with the frontend.