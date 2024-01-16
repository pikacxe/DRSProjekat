import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../../services/auth.service';
import { Router } from '@angular/router';
import { ProfileService } from '../../../services/profile.service';
import { finalize } from 'rxjs';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss',
})
export class HeaderComponent {
  isAdmin = false;

  constructor(
    private authService: AuthService,
    private router: Router,
    private profileService: ProfileService
  ) {}

  logOut() {
    this.authService.logOut();
    this.router.navigate(['']);
  }

  goToProfileEdit() {
    this.router.navigate(['/edit_profile']);
  }

  goToHomePage() {
    this.profileService.getUser(this.authService.getToken() + '')
    .pipe(
      finalize(() => {
        this.isAdmin ? this.router.navigate(['/main_page_admin']) : this.router.navigate(['/main_page']);
      })
    )
    .subscribe({
      next: (res) => {
        this.isAdmin = res.is_admin;
      }
    })
  }
}
