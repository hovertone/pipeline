import hou
import time
# def main():
#     operation = hou.InterruptableOperation('Doing Work', long_operation_name ='Starting Tasks', open_interrupt_dialog = True)
#     operation.__enter__()
#     try:
#         operation.updateLongProgress(0.1, 'test')
#         time.sleep(4)
#         operation.updateLongProgress(0.2, 'test')
#         time.sleep(4)
#         operation.__exit__(None, None, None)
#     except hou.OperationInterrupted:
#         operation.__exit__(None, None, None)

# def main():
#     num_tasks = 3
#     with hou.InterruptableOperation(
#             "Performing Tasks", open_interrupt_dialog=True) as operation:
#         for i in range(num_tasks):
#             # if hou.OperationInterrupted:
#             #     return
#             print 'AAAAA', i
#             time.sleep(2)
#             percent = float(i) / float(num_tasks)
#             print percent
#             operation.updateProgress(percent)

# def main():
#     num_tasks = 3
#     num_subtasks = 2
#     # Start the overall, long operation.
#     with hou.InterruptableOperation(
#             "Performing", "Performing Tasks",
#             open_interrupt_dialog=True) as operation:
#         for i in range(num_tasks):
#             # Update long operation progress.
#             overall_percent = float(i) / float(num_tasks)
#             operation.updateLongProgress(overall_percent)
#
#             print '%s' % i
#
# #             # Start the sub-operation.
# #             with hou.InterruptableOperation(
# #                     "Performing Task %i" % i) as suboperation:
# #                 for j in range(num_subtasks):
# #                     # Update sub-operation progress.
# #                     percent = float(j) / float(num_subtasks)
# #                     suboperation.updateProgress(percent)
# #
# #                     print '%s %s' % (i, j)
# #                     #
# #                     # PERFORM SUBTASK HERE.
# # #                     #

def main():
    # Create an interruptable operation.
    operation = hou.InterruptableOperation('Doing Work', long_operation_name='Starting Tasks', open_interrupt_dialog=True)

    # Start the operation. This will pop-up the progress bar dialog after a second or two.
    operation.__enter__()

    # Execute tasks. Periodically update the progress percentage and message in the progress bar.
    num_tasks = 10
    for i in range(num_tasks):
        # Do task work here. For this example, just sleep for a second.
        time.sleep(1)

        percent = float(i) / float(num_tasks)
        try:
            operation.updateLongProgress(percent, 'Finished task %i' % (i + 1))
        except hou.OperationInterrupted:
            print 'ABORTED BY USER'
            operation.__exit__(None, None, None)
            return

    # Stop the operation. This closes the progress bar dialog.
    operation.__exit__(None, None, None)