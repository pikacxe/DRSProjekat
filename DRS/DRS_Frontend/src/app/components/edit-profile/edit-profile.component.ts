import { Component, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { LoadingService } from '../../services/loading.service';
import { ProfileService } from '../../services/profile.service';
import { finalize } from 'rxjs';
import { MatDialog } from '@angular/material/dialog';
import { ChangePasswordDialogComponent } from '../dialogs/change-password-dialog/change-password-dialog.component';
import { HotToastService } from '@ngneat/hot-toast';

@Component({
  selector: 'app-edit-profile',
  templateUrl: './edit-profile.component.html',
  styleUrl: './edit-profile.component.scss',
})
export class EditProfileComponent implements OnInit {
  profileForm: FormGroup;
  hide1 = true;
  hide2 = true;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private loadingService: LoadingService,
    private profileService: ProfileService,
    private dialog: MatDialog,
    private toaster: HotToastService,
  ) {}

  ngOnInit(): void {
    this.profileForm = this.fb.group({
      first_name: new FormControl('', [Validators.required]),
      last_name: new FormControl('', [Validators.required]),
      address: new FormControl('', [Validators.required]),
      city: new FormControl('', [Validators.required]),
      country: new FormControl('', [Validators.required]),
      phone_number: new FormControl('', [Validators.required]),
      email: new FormControl('', [
        Validators.email,
        Validators.required,
        Validators.pattern(/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{1,5})+$/),
      ]),
    });

    this.loadUserData();
  }

  loadUserData() {
    this.loadingService.setLoadingState(true);
    this.profileService.getUser(this.authService.getToken() + '')
    .pipe(
      finalize(() => {
        this.loadingService.setLoadingState(false);
      })
    )
    .subscribe({
      next: (res) => {
        this.profileForm.patchValue({'first_name' : res.first_name});
        this.profileForm.patchValue({'last_name' : res.last_name});
        this.profileForm.patchValue({'address' : res.address});
        this.profileForm.patchValue({'city' : res.city});
        this.profileForm.patchValue({'country' : res.country});
        this.profileForm.patchValue({'phone_number' : res.phone_number});
        this.profileForm.patchValue({'email' : res.email});
      }
    })
  }

  save() {
    this.loadingService.setLoadingState(true);
    this.profileService.updateProfile(this.profileForm.value, this.authService.getToken() + '')
    .pipe(
      finalize(() => {
        this.loadingService.setLoadingState(false);
        this.loadUserData();
      })
    )
    .subscribe({
      next: (res) => {
        this.toaster.success('Profile updated successfully.');
      },
      error: (err) => {
        console.log(err.error);
      }
    })
  }

  openChangePasswordDialog() {
    this.dialog.open(ChangePasswordDialogComponent, {
      panelClass: 'custom-mat-dialog',
    });
  }
}
