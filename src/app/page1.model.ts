export class custDetails {
    userId: String;
    customerId: Number;
    date: String;
    modelId: String;
    name: String;
    modelName: String

    constructor(
        userId: String,
        customerId: Number,
        date: String,
        modelId: String,
        name: String,
        modelName: String
    ) {
        this.userId = userId;
        this.customerId = customerId;
        this.date=date;
        this.modelId= modelId;
        this.name= name;
        this.modelName=modelName;
     }
}