open util/ordering[Time]

sig Time {}

sig User {
  -- current place in time
  , at: Page one -> Time

  -- all visited pages
  , history: Page -> Time
}

sig Page {
  -- pages reachable from this page
  link: set Page
}

pred goto[u: User, p: Page, t, t': Time] {
  -- valid page to change to
  p in u.at.t.link

  -- change pages
  p = u.at.t'

  -- save new page in history
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
