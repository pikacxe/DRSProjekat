import { Component, OnInit, Inject } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { LoadingService } from '../../../services/loading.service';
import { HotToastService } from '@ngneat/hot-toast';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { TransactionService } from '../../../services/transaction.service';
import { AuthService } from '../../../services/auth.service';
import { finalize } from 'rxjs';

@Component({
  selector: 'app-new-transaction-dialog',
  templateUrl: './new-transaction-dialog.component.html',
  styleUrl: './new-transaction-dialog.component.scss'
})
export class NewTransactionDialogComponent implements OnInit{

  newTransactionForm: FormGroup;

  selectedValue = 'RSD';

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private dialogRef: MatDialogRef<NewTransactionDialogComponent>,
    private fb: FormBuilder,
    private transactionService: TransactionService,
    private authService: AuthService,
    private loadingService: LoadingService,
    private toaster: HotToastService,
  ){}

  ngOnInit(): void {
    this.newTransactionForm = this.fb.group({
      currency: new FormControl('', [Validators.required]),
      amount: new FormControl('', [Validators.required, Validators.pattern(/^\d+\.?\d*$/)]),
      recipient_card_number: new FormControl('', [Validators.required]),
      recipient_email: new FormControl('', [
        Validators.email,
        Validators.required,
        Validators.pattern(/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{1,5})+$/),
      ]),
      recipient_first_name: new FormControl('', [Validators.required]),
      recipient_last_name: new FormControl('', [Validators.required]),     
    })
  }

  createTransaction() {
    // const amountControl = this.newTransactionForm.get('amount');
    // this.newTransactionForm.controls['amount'].setValue(parseFloat(amountControl?.value));
    this.loadingService.setLoadingState(true);
    const dataToSend = {
      sender_card_number: this.data.SenderCardNumber,
      ...this.newTransactionForm.value,
    }

    this.transactionService.createTransaction(dataToSend, this.authService.getToken() +'')
    .pipe(
      finalize(() => {
        this.loadingService.setLoadingState(false);
      })
      )
      .subscribe({
        next: (res) => {
          this.toaster.success('Transaction completed');
          this.dialogRef.close();
      },
      error: (err) => {
        this.toaster.error(err.error.message);
      }
    })
  }

}
