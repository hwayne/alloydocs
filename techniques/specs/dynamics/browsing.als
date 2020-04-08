open util/ordering[Time]

sig Time {}

sig User {
  , at: Page one -> Time
  , history: Page -> Time
}

sig Page {
  link: set Page
}

pred goto[u: User, p: Page, t, t': Time] {
  p in u.at.t.link
  p = u.at.t'
  u.history.t' = u.history.t + p
}

pred stay[u: User, t, t': Time] {
  u.at.t' = u.at.t
  u.history.t' = u.history.t
}

fact trace {
  -- everybody starts with their initial page in history
  at.first = history.first 
  all t: Time - last |
    let t' = t.next {
      all u: User |
        u.stay[t, t'] or
        some p: Page | u.goto[p, t, t']
    }
}
