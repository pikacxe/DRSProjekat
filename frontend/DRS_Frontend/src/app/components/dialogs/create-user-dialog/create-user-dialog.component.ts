import { Component } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { AdminService } from '../../../services/admin.service';
import { HotToastService } from '@ngneat/hot-toast';
import { LoadingService } from '../../../services/loading.service';
import { AuthService } from '../../../services/auth.service';
import { MatDialogRef } from '@angular/material/dialog';
import { finalize } from 'rxjs';

@Component({
  selector: 'app-create-user-dialog',
  templateUrl: './create-user-dialog.component.html',
  styleUrl: './create-user-dialog.component.scss'
})
export class CreateUserDialogComponent {
  profileForm: FormGroup;


  constructor(
    private fb : FormBuilder,
    private adminService : AdminService,
    private loadingService : LoadingService,
    private toaster : HotToastService,
    private authService : AuthService,
    private dialogRef: MatDialogRef<CreateUserDialogComponent>,

  ){}
  ngOnInit(): void {
    this.profileForm = this.fb.group({
      first_name: new FormControl('', [Validators.required]),
      last_name: new FormControl('', [Validators.required]),
      address: new FormControl('', [Validators.required]),
      city: new FormControl('', [Validators.required]),
      country: new FormControl('', [Validators.required]),
      phone_number: new FormControl('', [Validators.required]),
      password: new FormControl('', [Validators.required]),
      email: new FormControl('', [
        Validators.email,
        Validators.required,
        Validators.pattern(/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{1,5})+$/),
      ]),
    });
  }

  createUser(){
    this.loadingService.setLoadingState(true);
    this.adminService.createUser(this.profileForm.value, this.authService.getToken() + '')
    .pipe(
      finalize(
        () => {this.loadingService.setLoadingState(false)}
      )
    )
    .subscribe(
      {next : (res) => {
        this.toaster.success("User registred successfully");
        this.dialogRef.close(true);
      },
      error : (err) => {
        this.toaster.error(err.error.message);
      }
    }
    )
  }
}
