from django.db.models.signals import post_save
from django.dispatch import receiver

from labsystem.laboratory.models import Result, ResultLine, Analysis


# @receiver(post_save, sender=Result)
# def create_result_lines(sender, instance, created, **kwargs):
#     if created:
#         analysis_lines = instance.analysis.analysis_field
#         for result_line in analysis_lines:
#             line = ResultLine(
#                 name=result_line.name,
#                 value=None,
#                 comment=None,
#                 result_id=instance.pk,
#                 analysis_field_id=analysis_lines.pk,
#             )
#             line.save()

@receiver(post_save, sender=Result)
def create_result_lines(sender, instance, created, **kwargs):
    if created:
        analysis_id = instance.analysis.id
        analysis_lines = Analysis.objects.get(pk=analysis_id).analysis_field.all()
        for result_line in analysis_lines:
            line = ResultLine(
                name=result_line.name,
                value=None,
                comment=None,
                result=instance,
                analysis_field=result_line,
            )
            line.save()
