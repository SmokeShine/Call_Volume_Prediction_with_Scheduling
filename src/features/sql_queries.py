"""
Contains queries to be used for training and prediction
"""

import logging
import logging.config
import pprint
PP = pprint.PrettyPrinter(indent=8)
LOGGER = logging.getLogger(__name__)
class Queries:
    """
    Dynamic Query Creation
    """
    def __init__(self, lag=20, days_to_predict=30):
        self.lag = str(lag)
        self.days_to_predict = str(days_to_predict)
        self.sql_calls_received = """
                            SELECT call_date, 
                                   Count(DISTINCT call_id) AS calls_received 
                            FROM   (SELECT * 
                                    FROM   pe_consumer_ot.ozonetel_calls_dump 
                                    WHERE  Date(call_date) BETWEEN ( '2019-07-01' ) AND ( '2019-12-31' ) 
                                           AND call_type = 'Inbound' 
                                           AND Lower(skill) LIKE '%voice_support%') callsdata 
                                   INNER JOIN (SELECT * 
                                               FROM   pe_consumer_fd.tickets 
                                               WHERE  source = 3) tickets 
                                           ON RIGHT(callsdata.call_id, 16) = tickets.cf_ucid 
                            GROUP  BY 1 
                            ORDER  BY 1
                            """
#         LOGGER.info(PP.pprint(self.sql_calls_received))
        self.sql_orders_placed = """
                    SELECT DISTINCT fo.order_placed_date, 
                                    Trim(To_char(fo.order_placed_date, 'Day')) AS dayofweek, 
                                    Count(DISTINCT CASE 
                                                     WHEN foc.user_type_monthly NOT IN 
                                                          ( 'Old User' ) THEN 
                                                     fo.order_id 
                                                   END)                     AS new_user, 
                                    Count(DISTINCT CASE 
                                                     WHEN foc.user_type_monthly IN ( 'Old User' ) 
                                                   THEN fo.order_id 
                                                   END)                     AS old_user, 
                                    Count(DISTINCT CASE 
                                                     WHEN fo.is_courier THEN fo.order_id 
                                                   END)                     AS courier_order, 
                                    Count(DISTINCT CASE 
                                                     WHEN NOT fo.is_courier THEN fo.order_id 
                                                   END)                     AS Non_courier_order, 
                                    Count(DISTINCT CASE 
                                                     WHEN NOT fo.is_delayed THEN fo.order_id 
                                                   END)                     AS Non_Delayed, 
                                    Count(DISTINCT CASE 
                                                     WHEN fo.is_delayed THEN fo.order_id 
                                                   END)                     AS Delayed, 
                                    Count(DISTINCT CASE 
                                                     WHEN fo.is_jit THEN fo.order_id 
                                                   END)                     AS JIT, 
                                    Count(DISTINCT CASE 
                                                     WHEN NOT fo.is_jit THEN fo.order_id 
                                                   END)                     AS Non_JIT 
                    FROM   data_model.f_order fo 
                           INNER JOIN data_model.f_order_consumer foc 
                                   ON fo.order_id = foc.order_id 
                    WHERE  fo.order_placed_date BETWEEN ( '2019-05-01' ) AND ( '2019-12-31' ) 
                    GROUP  BY 1, 
                              2 
                    ORDER  BY 1
                    """
#         LOGGER.info(PP.pprint(self.sql_orders_placed))
        self.sql_weekly_shape = """
                        SELECT Trim(To_char(call_date, 'Day')) as dayofweek, 
                               Extract(hour FROM start_time)||rpad(30*(extract(minute FROM start_time)::int / 30),2,0) AS Slot,
                               Count(DISTINCT call_id) as TotalCalls
                        FROM   pe_consumer_ot.ozonetel_calls_dump 
                        WHERE  Date(call_date) BETWEEN ( '2019-12-01' ) AND ( '2019-12-31' ) 
                               AND call_type = 'Inbound' 
                               AND Lower(skill) LIKE '%voice_support%' 
                        GROUP  BY 1, 
                                  2    
                        """
#         LOGGER.info(PP.pprint(self.sql_weekly_shape))
        self.sql_prediction_input = """
                    SELECT DISTINCT fo.order_placed_date, 
                                    Trim(To_char(fo.order_placed_date, 'Day')) AS dayofweek, 
                                    Count(DISTINCT CASE 
                                                     WHEN foc.user_type_monthly NOT IN 
                                                          ( 'Old User' ) THEN 
                                                     fo.order_id 
                                                   END)                     AS new_user, 
                                    Count(DISTINCT CASE 
                                                     WHEN foc.user_type_monthly IN ( 'Old User' ) 
                                                   THEN fo.order_id 
                                                   END)                     AS old_user, 
                                    Count(DISTINCT CASE 
                                                     WHEN fo.is_courier THEN fo.order_id 
                                                   END)                     AS courier_order, 
                                    Count(DISTINCT CASE 
                                                     WHEN NOT fo.is_courier THEN fo.order_id 
                                                   END)                     AS Non_courier_order, 
                                    Count(DISTINCT CASE 
                                                     WHEN NOT fo.is_delayed THEN fo.order_id 
                                                   END)                     AS Non_Delayed, 
                                    Count(DISTINCT CASE 
                                                     WHEN fo.is_delayed THEN fo.order_id 
                                                   END)                     AS Delayed, 
                                    Count(DISTINCT CASE 
                                                     WHEN fo.is_jit THEN fo.order_id 
                                                   END)                     AS JIT, 
                                    Count(DISTINCT CASE 
                                                     WHEN NOT fo.is_jit THEN fo.order_id 
                                                   END)                     AS Non_JIT 
                    FROM   data_model.f_order fo 
                           INNER JOIN data_model.f_order_consumer foc 
                                   ON fo.order_id = foc.order_id 
                    WHERE  fo.order_placed_date >= ( '2019-05-01' )  
                    GROUP  BY 1, 
                              2 
                    ORDER  BY 1
                    """
#         LOGGER.info(PP.pprint(self.sql_prediction_input))
