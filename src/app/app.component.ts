import { Component } from '@angular/core';
import {AppService}  from './app.service';
import {custDetails} from './page1.model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'angular-forms';
  cust = [];
  errorMsg:string;
  errorFlag: boolean=false;
  constructor(private appService:AppService){}

  fetchCustData(){
    this.appService.getCust().subscribe((data: custDetails []) => { this.cust =data},
    (error) =>  {this.errorMsg = error; this.errorFlag = true})
  }


  ngOnInit(){
    this.fetchCustData(); 
  }
}
