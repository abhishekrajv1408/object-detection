import cv2

from get_background import get_background

cap = cv2.VideoCapture("input/video_1.mp4")

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
save_name = f"outputs/output.mp4"
out = cv2.VideoWriter(
    save_name,
    cv2.VideoWriter_fourcc(*'mp4v'), 10,
    (frame_width, frame_height)
)
background = get_background("input/video_1.mp4")
background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
frame_count = 0
consecutive_frame = 4
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        frame_count += 1
        orig_frame = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if frame_count % consecutive_frame == 0 or frame_count == 1:
            frame_diff_list = []
        frame_diff = cv2.absdiff(gray, background)
        ret, thres = cv2.threshold(frame_diff, 50, 255, cv2.THRESH_BINARY)
        dilate_frame = cv2.dilate(thres, None, iterations=2)
        frame_diff_list.append(dilate_frame)
        if len(frame_diff_list) == consecutive_frame:
            sum_frames = sum(frame_diff_list)
            contours, hierarchy = cv2.findContours(
                sum_frames, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for i, cnt in enumerate(contours):
                cv2.drawContours(frame, contours, i, (0, 0, 255), 3)
            for contour in contours:
                if cv2.contourArea(contour) < 500:
                    continue
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(orig_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            cv2.imshow('Detected Objects', orig_frame)
            out.write(orig_frame)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
    else:
        break
cap.release()
cv2.destroyAllWindows()
