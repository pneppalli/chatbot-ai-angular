// Zone.js is required by Angular for change detection and many core features.
// Ensure it's imported before bootstrapping the Angular application.
import 'zone.js';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppModule } from './app/app.module';

platformBrowserDynamic().bootstrapModule(AppModule)
  .catch(err => console.error(err));
