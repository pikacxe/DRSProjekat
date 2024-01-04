import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddFundsDialogComponent } from './add-funds-dialog.component';

describe('AddFundsDialogComponent', () => {
  let component: AddFundsDialogComponent;
  let fixture: ComponentFixture<AddFundsDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AddFundsDialogComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(AddFundsDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
