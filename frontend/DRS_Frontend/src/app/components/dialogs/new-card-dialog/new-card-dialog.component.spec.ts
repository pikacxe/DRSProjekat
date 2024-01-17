import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewCardDialogComponent } from './new-card-dialog.component';

describe('NewCardDialogComponent', () => {
  let component: NewCardDialogComponent;
  let fixture: ComponentFixture<NewCardDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [NewCardDialogComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(NewCardDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
