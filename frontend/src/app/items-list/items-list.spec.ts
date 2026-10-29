import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ItemsList } from './items-list';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';

describe('ItemsList', () => {
  let component: ItemsList;
  let fixture: ComponentFixture<ItemsList>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ItemsList],
      providers: [provideHttpClient(), provideHttpClientTesting()],
    }).compileComponents();

    fixture = TestBed.createComponent(ItemsList);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
