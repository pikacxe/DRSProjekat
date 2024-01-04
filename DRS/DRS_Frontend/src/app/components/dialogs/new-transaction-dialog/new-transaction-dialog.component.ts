import { Component, OnInit, Inject } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { LoadingService } from '../../../services/loading.service';
import { HotToastService } from '@ngneat/hot-toast';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

interface Currency {
  value: string;
  viewValue: string;
}

@Component({
  selector: 'app-new-transaction-dialog',
  templateUrl: './new-transaction-dialog.component.html',
  styleUrl: './new-transaction-dialog.component.scss'
})
export class NewTransactionDialogComponent implements OnInit{

  newTransactionForm: FormGroup;

  selectedValue = 'dinar';

  currencies: Currency[] = [
    {value: 'euro', viewValue: 'Euro'},
    {value: 'dollar', viewValue: 'Dollar'},
    {value: 'dinar', viewValue: 'Dinar'},
  ];

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private dialogRef: MatDialogRef<NewTransactionDialogComponent>,
    private fb: FormBuilder,
    private loadingService: LoadingService,
    private toaster: HotToastService,
  ){}

  ngOnInit(): void {
    this.newTransactionForm = this.fb.group({
      Currency: new FormControl('', [Validators.required]),
      Amount: new FormControl('', [Validators.required, Validators.pattern(/^\d+\.?\d*$/)]),
      RecipientCardNumber: new FormControl('', [Validators.required]),
      RecipientEmail: new FormControl('', [
        Validators.email,
        Validators.required,
        Validators.pattern(/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{1,5})+$/),
      ]),
      RecipientFName: new FormControl('', [Validators.required]),
      RecipientLName: new FormControl('', [Validators.required]),     
    })
  }

  createTransaction() {
    const amountControl = this.newTransactionForm.get('Amount');
    this.newTransactionForm.controls['Amount'].setValue(parseFloat(amountControl?.value));
    
    const dataToShow = {
      SenderID: this.data.SenderID,
      SenderCardNumber: this.data.SenderCardNumber,
      ...this.newTransactionForm.value,
    }
    console.log(dataToShow);
    this.dialogRef.close();
  }

}
