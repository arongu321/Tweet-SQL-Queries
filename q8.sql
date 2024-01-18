  with T(month, tcnt) as (
    select strftime('%m', tdate), count(*) 
        from tweets
        where strftime('%Y', tdate)='2023' and replyto_w is null 
        group by strftime('%m', tdate)),
  REP(month, rep_cnt) as (
    select strftime('%m', tdate), count(*) 
        from tweets
        where strftime('%Y', tdate)='2023' and replyto_w is not null 
        group by strftime('%m', tdate)),
  RET(month, ret_cnt) as (
    select strftime('%m', rdate), count(*)
        from retweets
        where strftime('%Y', rdate)='2023'
        group by strftime('%m', rdate)),
  TREP(month, tcnt, rep_cnt) as (
    select T.month, tcnt, rep_cnt
    from T left outer join REP on T.month=REP.month
    union
    select REP.month, tcnt, rep_cnt
    from REP left outer join T on REP.month=T.month)
  select TREP.month, ifnull(tcnt,0) as tcnt, ifnull(rep_cnt,0)
         as rep_cnt, ifnull(ret_cnt,0) as ret_cnt,
	 ifnull(tcnt,0)+ifnull(rep_cnt,0)+ifnull(ret_cnt,0) as total
  from TREP left outer join RET on TREP.month=RET.month;
