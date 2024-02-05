import { Injectable } from '@angular/core';

@Injectable()
export class ContentService{
    content;
    constructor(){
        this.content = {};
    }
    
    setContent(val: object){
        this.content = val
    }

    getContent(){
        return this.content
    }

}