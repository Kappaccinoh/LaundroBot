function withinThirty(date_str, start_time_str, gmt) {
    let meeting_room_gmt = parseInt(gmt.slice(1,2))
    let curr_datetime_str = (new Date()).toString()
    let user_gmt = parseInt(curr_datetime_str.slice(30,31))
    let curr_month = curr_datetime_str.slice(4,7)
    curr_month = monthConvert(curr_month)
    let curr_day = curr_datetime_str.slice(8,10)
    let curr_year = curr_datetime_str.slice(11,15)
    let curr_min = parseInt(curr_datetime_str.slice(19,21))
    let curr_hour = parseInt(curr_datetime_str.slice(16,18))
    let curr_date_str = `${curr_year}-${curr_month}-${curr_day}`
    let is_same_date = false
    if (curr_date_str == date_str) {
        is_same_date = true
    }

    const new_curr_time = new Date();
    new_curr_time.setTime((curr_hour - user_gmt) * 60 * 60 * 1000 + curr_min * 60 * 1000)
    let start_time = new Date();
    let start_hour = parseInt(start_time_str.slice(0,2))
    let start_min = parseInt(start_time_str.slice(3,5))
    start_time.setTime((start_hour-meeting_room_gmt) * 60 * 60 * 1000 + start_min * 60 * 1000)

    let diff_minutes = (start_time-new_curr_time) / (1000 * 60)
    if (diff_minutes>=0 && diff_minutes<=30 && is_same_date) {
        return true
    } else {
        return false
    }




    
    
    
}

function monthConvert(month) {
    switch (month) {
      case 'Jan':
        return '01';
      case 'Feb':
        return '02';
      case 'Mar':
        return '03';
      case 'Apr':
        return '04';
      case 'May':
        return '05';
      case 'Jun':
        return '06';
      case 'Jul':
        return '07';
      case 'Aug':
        return '08';
      case 'Sep':
        return '09';
      case 'Oct':
        return '10';
      case 'Nov':
        return '11';
      case 'Dec':
        return '12';
      default:
        return '';
    }

  }
