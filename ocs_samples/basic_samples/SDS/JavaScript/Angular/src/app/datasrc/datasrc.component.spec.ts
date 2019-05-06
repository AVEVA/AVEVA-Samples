// datasrc.component.spec.ts
//

import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DatasrcComponent } from './datasrc.component';

describe('DatasrcComponent', () => {
  let component: DatasrcComponent;
  let fixture: ComponentFixture<DatasrcComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DatasrcComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DatasrcComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
