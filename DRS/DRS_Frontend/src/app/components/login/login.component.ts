import { Component, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';
import { HotToastService } from '@ngneat/hot-toast';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { LoadingService } from '../../services/loading.service';
import { finalize } from 'rxjs';
import { ProfileService } from '../../services/profile.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
})
export class LoginComponent implements OnInit {
  logInForm: FormGroup;
  hide = true;
  isAdmin: boolean;
  logInSuccess = false;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private loadingService: LoadingService,
    private toaster: HotToastService,
    private router: Router,
  ) {}

  ngOnInit(): void {
    this.logInForm = this.fb.group({
      email: new FormControl('', [
        Validators.email,
        Validators.required,
        Validators.pattern(/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{1,5})+$/),
      ]),
      password: new FormControl('', [Validators.required]),
    });
  }

  logIn() {
    if (this.logInForm.invalid) {
      this.toaster.error('Please fill out the form properly.');
      return;
    }
    this.loadingService.setLoadingState(true);

    this.authService
      .logIn(this.logInForm.value)
      .pipe(
        finalize(() => {
          this.loadingService.setLoadingState(false);
        })
      )
      .subscribe({
        next: (res) => {
          this.authService.setToken(res.access_token);
          res.is_admin
          ? this.router.navigate(['/main_page_admin'])
          : this.router.navigate(['/main_page']);
          this.toaster.success('Log in successfull');
        },
        error: (err) => {
          this.toaster.error(err.error.message);
        },
      });
  }
}
