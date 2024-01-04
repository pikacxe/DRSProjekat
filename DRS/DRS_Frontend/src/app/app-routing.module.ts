import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { MainPageComponent } from './components/main-page/main-page.component';
import { loginGuard } from './guards/login.guard';
import { MainPageAdminComponent } from './components/main-page-admin/main-page-admin.component';
import { EditProfileComponent } from './components/edit-profile/edit-profile.component';

const routes: Routes = [
  { path: '', component: LoginComponent },
  { path: 'main_page', component: MainPageComponent, canActivate: [loginGuard] },
  { path: 'main_page_admin', component: MainPageAdminComponent, canActivate: [loginGuard] },
  { path: 'edit_profile', component: EditProfileComponent, canActivate: [loginGuard] },

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
