import { Component, OnInit } from '@angular/core';
import { AdminService } from '../../services/admin.service';
import { AuthService } from '../../services/auth.service';
import { MatDialog } from '@angular/material/dialog';
import { LoadingService } from '../../services/loading.service';
import { HotToastService } from '@ngneat/hot-toast';
import { finalize } from 'rxjs';
import { CreateUserDialogComponent } from '../dialogs/create-user-dialog/create-user-dialog.component';

@Component({
  selector: 'app-manage-users',
  templateUrl: './manage-users.component.html',
  styleUrl: './manage-users.component.scss',
})
export class ManageUsersComponent implements OnInit {

  users: any[];
  constructor(
    private adminService: AdminService,
    private authService: AuthService,
    private dialog: MatDialog,
    private loadingService: LoadingService,
    private toaster: HotToastService,

  ) {}

  openDialog(){
    const dialogRef = this.dialog.open(CreateUserDialogComponent,{
      panelClass: 'custom-mat-dialog',
    });
    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.getAllUnverified();
      }
    });
  }

  ngOnInit(): void {
    this.getAllUnverified();
  }

  getAllUnverified(){
    this.adminService.getAllUnverified(this.authService.getToken() + '').subscribe({
      next: (res) =>{
        this.users = res;
      }
    })
  }

  verifyUser(userId:string) {
    this.loadingService.setLoadingState(true);
    let data = {
      user_id : userId
    }
    this.adminService.verifyUser(data, this.authService.getToken() + '')
    .pipe(
      finalize(
        () => {this.loadingService.setLoadingState(false)}
      )
    )
    .subscribe(
      {next : (res) => {
        this.toaster.success("User verified successfully");
        this.getAllUnverified();
      },
      error : (err) => {
        this.toaster.error(err.error.message);
      }
    }
    )
  }
}
