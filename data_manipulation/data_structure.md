```
document    
│
└───paragraph
│   │   bbox: (x1,y1,x2,y2)
│   │   texts: ['ax','bc',...]
│   │
│   └───line
│       │   bbox: (x1,y1,x2,y2)
│       │   texts: ['text1','text2',...]
│       │   
|       └───word
|           |   bbox: (x1,y1,x2,y2)
|           |   text: 'a'
|
|
└───title
│   │   bbox: (x1,y1,x2,y2)
│   │   texts: ['ax','bc',...]
│   │
│   └───line
│       │   bbox: (x1,y1,x2,y2)
│       │   texts: ['text1','text2',...]
│       │   
|       └───word
|           |   bbox: (x1,y1,x2,y2)
|           |   text: 'a'
|           
│   
└───table
│   │   bbox: (x1,y1,x2,y2)
│   │   texts: ['ax','bc',...]
│   │
│   └───cells
│       │   bbox: (x1,y1,x2,y2)
│       │   texts: ['text1','text2',...]
│       │   
|       └───word
|           |   bbox: (x1,y1,x2,y2)
|           |   text: 'a'
|
└───figure
│   │   bbox: (x1,y1,x2,y2)
|
└───formula
│   │   bbox: (x1,y1,x2,y2)
|
└───plot
│   │   bbox: (x1,y1,x2,y2)
```