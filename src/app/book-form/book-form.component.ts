import { Component, OnInit } from '@angular/core';
import { custDetails } from '../page1.model';

@Component({
  selector: 'book-form',
  templateUrl: './book-form.component.html',
  styleUrls: ['./book-form.component.css']
})
export class BookFormComponent implements OnInit {

  model = new custDetails('', 1,'','','','');;
 

  //constructor(private httpClient: HttpClient)  { }

  ngOnInit() {
  }
  get currentBook() { return JSON.stringify(this.model); }
}
