// Create a new subject for the authenticated user
query "subjects" verb=POST {
  api_group = "Subjects"
  auth = "user"

  input {
    text name filters=trim
    text? teacher filters=trim
    int? hours
  }

  stack {
    db.add subjects {
      data = {
        created_at: "now"
        name: $input.name
        teacher: $input.teacher
        hours: $input.hours
        user_id: $auth.id
      }
    } as $subject
  }

  response = $subject
  tags = ["edutrack:academic"]
  guid = "LRDtq_1zClBZpsMOFLZ9ndqVM34"
}
