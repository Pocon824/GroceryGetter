import { HttpClient } from '@angular/common/http';
import { Service, inject } from '@angular/core';
import { ItemSummary } from './items/item.models';

const baseUrl = 'http://localhost:8000';

@Service()
export class Items {
    private http = inject(HttpClient);

    getItems(query?: string) {
        return this.http.get<ItemSummary[]>(`${baseUrl}/api/items`, { params: query ? { q: query } : {}  });
    }
}
