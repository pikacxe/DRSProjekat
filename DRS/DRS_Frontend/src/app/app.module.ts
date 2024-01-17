import { NgModule } from '@angular/core';
import { BrowserModule, provideClientHydration } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './components/login/login.component';
import { HeaderComponent } from './components/shared/header/header.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MaterialModule } from './app-material.module';
import { HotToastModule } from '@ngneat/hot-toast';
import { MainPageComponent } from './components/main-page/main-page.component';
import { JWT_OPTIONS, JwtHelperService } from '@auth0/angular-jwt';
import { HttpClientModule } from '@angular/common/http';
import { SpinnerComponent } from './components/shared/spinner/spinner.component';
import { NewTransactionDialogComponent } from './components/dialogs/new-transaction-dialog/new-transaction-dialog.component';
import { AddFundsDialogComponent } from './components/dialogs/add-funds-dialog/add-funds-dialog.component';
import { MainPageAdminComponent } from './components/main-page-admin/main-page-admin.component';
import { NewCardDialogComponent } from './components/dialogs/new-card-dialog/new-card-dialog.component';
import { EditProfileComponent } from './components/edit-profile/edit-profile.component';
import { ChangePasswordDialogComponent } from './components/dialogs/change-password-dialog/change-password-dialog.component';
import { ConvertDialogComponent } from './components/dialogs/convert-dialog/convert-dialog.component';
import { ManageUsersComponent } from './components/manage-users/manage-users.component';
import { CreateUserDialogComponent } from './components/dialogs/create-user-dialog/create-user-dialog.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    HeaderComponent,
    MainPageComponent,
    SpinnerComponent,
    NewTransactionDialogComponent,
    AddFundsDialogComponent,
    MainPageAdminComponent,
    NewCardDialogComponent,
    EditProfileComponent,
    ChangePasswordDialogComponent,
    ConvertDialogComponent,
    ManageUsersComponent,
    CreateUserDialogComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MaterialModule,
    HttpClientModule,
    HotToastModule.forRoot(
      {
        position: 'bottom-center',
        duration: 3000,
        dismissible: true,
        style: { padding: '15px', marginBottom: '40px' }
      }
    ),
  ],
  providers: [
    JwtHelperService,
    {
      provide: JWT_OPTIONS,
      useValue: JWT_OPTIONS
    },
    provideClientHydration()
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
