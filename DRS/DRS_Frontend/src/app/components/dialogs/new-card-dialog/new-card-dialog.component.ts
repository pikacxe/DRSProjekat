import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { LoadingService } from '../../../services/loading.service';
import { HotToastService } from '@ngneat/hot-toast';
import { CardService } from '../../../services/card.service';
import { AuthService } from '../../../services/auth.service';
import { finalize } from 'rxjs';

@Component({
  selector: 'app-new-card-dialog',
  templateUrl: './new-card-dialog.component.html',
  styleUrl: './new-card-dialog.component.scss'
})
export class NewCardDialogComponent implements OnInit{
  newCardForm: FormGroup;

  constructor(
    private dialogRef: MatDialogRef<NewCardDialogComponent>,
    private fb: FormBuilder,
    private loadingService: LoadingService,
    private toaster: HotToastService,
    private cardService: CardService,
    private authService: AuthService,
  ){}

  ngOnInit(): void {
    this.newCardForm = this.fb.group({
      card_number: new FormControl('', [Validators.required]),  
    })
  }

  addCard() {
    this.loadingService.setLoadingState(true);
    this.cardService.addCard(this.newCardForm.value, this.authService.getToken() + '')
    .pipe(
      finalize(() => {
        this.loadingService.setLoadingState(false);
      })
    )
    .subscribe({
      next: (res) => {
        this.toaster.success('Card successfully added')
        this.dialogRef.close(true);
      },
      error: (err) => {
        this.toaster.error(err.error.message);
      }
    })
  }
}
