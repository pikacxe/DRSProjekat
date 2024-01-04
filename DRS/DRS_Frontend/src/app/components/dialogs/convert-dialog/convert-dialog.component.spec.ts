import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConvertDialogComponent } from './convert-dialog.component';

describe('ConvertDialogComponent', () => {
  let component: ConvertDialogComponent;
  let fixture: ComponentFixture<ConvertDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ConvertDialogComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ConvertDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
