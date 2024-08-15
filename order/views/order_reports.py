#!/usr/bin/python3
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from order.utils.reports import dailyReports, weeklyReports, monthlyReports

""" Sales Report endpoints """

class SalesReportView(APIView):
    """
        Sales Report Endpoint
        -> /orders/reports/sales
        -> Allowed methods [GET]
    """
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        """
        Generate daily, weekly and month sales reports

        Returns:
            -> 200 json data {
                "daily_report": {
                    "date": "1993/12/12",
                    "total_orders": 23,
                    "total_revenue": 356,
                    "orders": [{object},{object}]
                    },

                "weekly_report": {
                    "week_start": "1993/12/5",
                    "week_end": "1993/12/12",
                    "total_orders": 26,
                    "total_revenue": 3444,
                    "orders": [{object},{object}]
                    },

                "monthly_report": {
                    "monthly_start": "1993/11/4",
                    "monthly_end": "1993/12/3",
                    "total_orders": 26,
                    "orders": [{object},{object}]
                    }
                } 
            -> 500 json data {'message': 'an internal server error occurred!'}

        """
        # generate reports
        try:
            daily = dailyReports()
            weekly = weeklyReports()
            monthly = monthlyReports()

            # make a dictionary from the reports

            reports = {
                    "daily_report": daily.get('daily_report'),
                    "weekly_report": weekly.get('weekly_report'),
                    "monthly_report": monthly.get('monthly_report')
                    }

            return Response(reports, status=status.HTTP_200_OK)

        except Exception as e:
            print(e) # can be logged into a file
            return Response({'message': 'an internal server error occurred!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
