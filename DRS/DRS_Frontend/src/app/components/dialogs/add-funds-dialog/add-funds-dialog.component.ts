import { Component, Inject } from '@angular/core';
import { Currency } from '../../../interfaces/currency-interface';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { CurrencyRatesService } from '../../../services/currency-rates.service';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';
import { CardService } from '../../../services/card.service';
import { LoadingService } from '../../../services/loading.service';
import { HotToastService } from '@ngneat/hot-toast';
import { AuthService } from '../../../services/auth.service';
import { finalize } from 'rxjs';

@Component({
  selector: 'app-add-funds-dialog',
  templateUrl: './add-funds-dialog.component.html',
  styleUrl: './add-funds-dialog.component.scss',
})
export class AddFundsDialogComponent {
  selectedValue = 'RSD';
  currencies: Currency[] = [];

  addFundsForm: FormGroup;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private dialogRef: MatDialogRef<AddFundsDialogComponent>,
    private fb: FormBuilder,
    private ratesService: CurrencyRatesService,
    private cardService: CardService,
    private authService: AuthService,
    private loadingService: LoadingService,
    private toaster: HotToastService
  ) {}

  ngOnInit(): void {
    this.addFundsForm = this.fb.group({
      currency: new FormControl('', [Validators.required]),
      amount: new FormControl('', [Validators.required]),
    });

    this.ratesService.currency_rates$.subscribe({
      next: (res) => {
        this.currencies = res;
      },
    });
  }

  addFunds() {
    this.loadingService.setLoadingState(true);

    this.cardService
      .addFunds(
        this.addFundsForm.value,
        this.data.DepositCardNumber,
        this.authService.getToken() + ''
      )
      .pipe(
        finalize(() => {
          this.loadingService.setLoadingState(false);
        })
      )
      .subscribe({
        next: (res) => {
          this.toaster.success('Deposit successful');
          this.dialogRef.close(true);
        },
        error: (err) => {
          this.toaster.error(err.error.message);
        },
      });
  }
}
