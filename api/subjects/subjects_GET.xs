// List all subjects belonging to the authenticated user
query "subjects" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
  }

  stack {
    db.query subjects {
      where = $db.subjects.user_id == $auth.id
      return = {type: "list"}
    } as $user_subjects
  }

  response = $user_subjects
  tags = ["edutrack:academic"]
  guid = "2hlLlfAmvz-laij8U4fPdbjTRAs"
}
