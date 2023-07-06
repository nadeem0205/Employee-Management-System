from django.views.generic import ListView
from .models import APILogEntry
from django.http import JsonResponse
from datetime import datetime


class APILogEntryListView(ListView):
    """
    To get log entries of all APIs in this project

    Returns JSON response
    """
    model = APILogEntry
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by date
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")

        # If both start date and end date are provided
        if start_date and end_date:
            try:
                # print(1)
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                print(start_date, end_date)
                queryset = queryset.filter(
                    created_at__date__gte=start_date, created_at__date__lte=end_date
                )
                # print(queryset)
            except ValueError:
                pass

        # If start date is provided
        if start_date and not end_date:
            try:
                # print(2)
                print(start_date)
                queryset = queryset.filter(created_at__gte=start_date)
            except ValueError:
                pass

        # If end date is provided
        if end_date and not start_date:
            try:
                # print(3)
                queryset = queryset.filter(created_at__date__lte=end_date)
            except ValueError:
                pass

        return queryset

    def render_to_response(self, context, **response_kwargs):
        # print(context)
        log_entries = context["object_list"]
        # print(log_entries)
        data = {
            "results": [
                {
                    "id": log_entry.id,
                    "method": log_entry.method,
                    "path": log_entry.path,
                    "status_code": log_entry.status_code,
                    "response_time": log_entry.response_time,
                    # 'response_content': log_entry.response_content,
                    "created_at": log_entry.created_at,
                }
                for log_entry in log_entries
            ],
            "logs_per_page": log_entries.count(),
            "total_pages": context["paginator"].num_pages,
            "has_previous": context["page_obj"].has_previous(),
            "has_next": context["page_obj"].has_next(),
            "previous_page_number": context["page_obj"].previous_page_number()
            if context["page_obj"].has_previous()
            else None,
            "next_page_number": context["page_obj"].next_page_number()
            if context["page_obj"].has_next()
            else None,
        }

        return JsonResponse(data, **response_kwargs)
