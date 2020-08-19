data = {
  "questions": [
    {
      "id": 100,
      "type": "select-many",
      "text": "Question 1 title ",
      "is_mandatory": "true",
      "answers": [
        {
          "id": 101,
          "text": "option 1",
          "questions": [
            {
              "id": 400,
              "type": "text",
              "text": "Sub question text title",
              "is_mandatory": "true"
            },
            {
              "id": 500,
              "type": "select-one",
              "text": "SubQuestion 2 title ",
              "is_mandatory": "true",
              "answers": [
                {
                  "id": 501,
                  "text": "SubQuestion option 1",
                  "questions": []
                },
                {
                  "id": 502,
                  "text": "SubQuestion option 2",
                  "questions": []
                }
              ]
            }
          ]
        },
        {
          "id": 102,
          "text": "option 2",
          "questions": []
        },
        {
          "id": 103,
          "text": "option 3",
          "questions": [
            {
              "id": 600,
              "type": "select-one",
              "text": "SubQuestion 3 title ",
              "is_mandatory": "false",
              "answers": [
                {
                  "id": 601,
                  "text": "SubQuestion option 1"
                },
                {
                  "id": 602,
                  "text": "SubQuestion option 2"
                }
              ]
            }
          ]
        },
        {
          "id": 104,
          "text": "option 4",
          "questions": []
        },
        {
          "id": 105,
          "text": "option 5",
          "questions": []
        },
        {
          "id": 106,
          "text": "option 6",
          "questions": []
        }
      ]
    },
    {
      "id": 200,
      "type": "select-one",
      "text": "Question 2 title ",
      "is_mandatory": "false",
      "answers": [
        {
          "id": 201,
          "text": "q2 option 1",
          "questions": []
        },
        {
          "id": 202,
          "text": "q2 option 2",
          "questions": []
        }
      ]
    },
    {
      "id": 300,
      "type": "text",
      "text": "Expalin your requirement in deatil",
      "is_mandatory": "true"
    }
  ]
}