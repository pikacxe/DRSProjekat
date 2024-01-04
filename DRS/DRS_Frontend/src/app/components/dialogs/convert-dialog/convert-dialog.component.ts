import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Currency } from '../../../interfaces/currency-interface';
import { CurrencyRatesService } from '../../../services/currency-rates.service';

@Component({
  selector: 'app-convert-dialog',
  templateUrl: './convert-dialog.component.html',
  styleUrl: './convert-dialog.component.scss',
})
export class ConvertDialogComponent implements OnInit {
  selectedValue = 'RSD';
  currencies: Currency[] = [];
  balanceInRsd: number;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private ratesService: CurrencyRatesService
  ) {}

  ngOnInit(): void {
    this.ratesService.currency_rates$.subscribe({
      next: (res) => {
        this.currencies = res;
      },
    });
    this.balanceInRsd = this.data.balance;
  }

  calculateBalance() {
    let selectedCurrency = this.currencies.find(
      (currency) => currency.currency === this.selectedValue
    );
    if (selectedCurrency) {
      this.data.balance = this.balanceInRsd;
      this.data.balance = (
        this.data.balance / selectedCurrency.exchange
      ).toFixed(2);
    }
  }
}
