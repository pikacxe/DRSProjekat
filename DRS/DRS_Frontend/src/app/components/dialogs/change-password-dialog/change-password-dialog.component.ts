import { Component, OnInit } from '@angular/core';
import { LoadingService } from '../../../services/loading.service';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ProfileService } from '../../../services/profile.service';
import { AuthService } from '../../../services/auth.service';
import { finalize } from 'rxjs';
import { HotToastService } from '@ngneat/hot-toast';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-change-password-dialog',
  templateUrl: './change-password-dialog.component.html',
  styleUrl: './change-password-dialog.component.scss',
})
export class ChangePasswordDialogComponent implements OnInit {
  hide1 = true;
  hide2 = true;
  changePwForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private loadingService: LoadingService,
    private profileService: ProfileService,
    private authService: AuthService,
    private toaster: HotToastService,
    private dialogRef: MatDialogRef<ChangePasswordDialogComponent>
  ) {}

  ngOnInit(): void {
    this.changePwForm = this.fb.group({
      old_password: new FormControl('', [Validators.required]),
      new_password: new FormControl('', [Validators.required]),
    })
  }

  changePassword() {
    this.loadingService.setLoadingState(true);
    this.profileService.changePassword(this.changePwForm.value, this.authService.getToken() +'')
    .pipe(
      finalize(() => {
        this.loadingService.setLoadingState(false);
      })
    )
    .subscribe({
      next: (res) => {
        this.toaster.success('Password changed successfully.');
        this.dialogRef.close();
      },
      error: (err) => {
        this.toaster.error(err.error.message);
      }
    })
  }
}
