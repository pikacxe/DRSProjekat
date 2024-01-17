import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { NewTransactionDialogComponent } from '../dialogs/new-transaction-dialog/new-transaction-dialog.component';
import { LoadingService } from '../../services/loading.service';
import { HotToastService } from '@ngneat/hot-toast';
import { AddFundsDialogComponent } from '../dialogs/add-funds-dialog/add-funds-dialog.component';
import { NewCardDialogComponent } from '../dialogs/new-card-dialog/new-card-dialog.component';
import { CardService } from '../../services/card.service';
import { AuthService } from '../../services/auth.service';
import { finalize } from 'rxjs';
import { Currency } from '../../interfaces/currency-interface';
import { CurrencyService } from '../../services/currency.service';
import { CurrencyRatesService } from '../../services/currency-rates.service';
import { ConvertDialogComponent } from '../dialogs/convert-dialog/convert-dialog.component';

@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styleUrl: './main-page.component.scss',
})
export class MainPageComponent implements OnInit {
  cards: any[];
  isLonger = false;

  currencies: Currency[] = [];

  isVerified = true;

  constructor(
    private dialog: MatDialog,
    private loadingService: LoadingService,
    private toaster: HotToastService,
    private cardService: CardService,
    private authService: AuthService,
    private currencyService: CurrencyService,
    private ratesService: CurrencyRatesService
  ) {}

  ngOnInit(): void {
    this.currencyService.getCurrencyRates().subscribe({
      next: (res) => {
        let data = res.rates.map((response: any) => ({
          currency: response.code,
          exchange: response.exchange_middle,
        }));
        data.push({ currency: 'RSD', exchange: 1 });
        data.sort((a: any, b: any) => a.currency.localeCompare(b.currency));
        this.ratesService.setCurrencyRates(data);
      },
    });

    this.ratesService.currency_rates$.subscribe({
      next: (res) => {
        this.currencies = res;
      },
    });
    this.getAllCards();
  }

  openNewTransactionDialog(cardNumber: string, balances: any[]) {
    this.dialog.open(NewTransactionDialogComponent, {
      panelClass: 'custom-mat-dialog',
      data: {
        SenderCardNumber: cardNumber,
        SenderCurrencies: balances,
      },
    });
  }

  openConvertDialog(balanceToSend: any) {
    this.dialog.open(ConvertDialogComponent, {
      panelClass: 'custom-mat-dialog',
      data: {
        balance: balanceToSend,
      },
    });
  }

  openAddFundsDialog(cardNumber: string) {
    const dialogRef = this.dialog.open(AddFundsDialogComponent, {
      panelClass: 'custom-mat-dialog',
      data: {
        DepositCardNumber: cardNumber,
      },
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.getAllCards();
      }
    });
  }

  openNewCardDialog() {
    const dialogRef = this.dialog.open(NewCardDialogComponent, {
      panelClass: 'custom-mat-dialog',
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.getAllCards();
      }
    });
  }

  getAllCards() {
    this.loadingService.setLoadingState(true);
    this.cardService
      .getAllCards(this.authService.getToken() + '')
      .pipe(
        finalize(() => {
          this.loadingService.setLoadingState(false);
        })
      )
      .subscribe({
        next: (res) => {
          this.cards = res;
          if (this.cards.length > 1) {
            this.isLonger = true;
          }
          this.cards.length == 0
            ? (this.isVerified = false)
            : (this.isVerified = true);
        },
      });
  }
}
