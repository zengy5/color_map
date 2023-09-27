import open3d as o3d
import numpy as np
import color_cloud
import cv2

pointcloud_file = 'data/pcds/0824.pcd'
key_frame = 'result_frame.txt'
bef_pic_name = 'data/pics/0.jpg'
aft_pic_name = 'data/pics/1691140933.024831.jpg'
camera_intrinsic = np.float64([
    [911.3619384765625, 0.0, 652.8096923828125],
    [ 0.0, 911.00202141601562, 364.7060852050781],
    [0.0, 0.0, 1.0]
])
distCoeffs = np.float64([0.0, 0.0, 0.0, 0.0, 0.0])

lidar_to_camera_extrinsic = np.float64([
    [0.330321,-0.943867,-0.00202757, 0.0908665],
    [0.252695,0.090504,-0.963304, 0.0388712],
    [0.909414,0.317687,0.268406, -0.137543],
    [0, 0, 0, 1]
])

if __name__ == "__main__":
    pcd = o3d.io.read_point_cloud(pointcloud_file)
    points = np.asarray(pcd.points)
    num_points = points.shape[0]
    point_colors_bgr = np.ones((num_points, 3), dtype=np.uint8)
    # pcd.colors = o3d.utility.Vector3dVector(point_colors_bgr)
    # point_colors_bgr = np.asarray(pcd.colors)
    Trans, Stamps= color_cloud.key_frame_extract(key_frame)
    _,rvec,tvec = color_cloud.get_R_and_T(lidar_to_camera_extrinsic)
    
    test_pose = Trans[270]
    print(Stamps[270])
    
    # Color the PCD
    image = cv2.imread(bef_pic_name)
    point_matrix = np.ones((num_points, 4))
    point_matrix[:, :3] = points
    point_2d, _ = cv2.projectPoints(points, rvec, tvec, camera_intrinsic, distCoeffs)
    point_pixel_coords = point_2d.astype(int)

    result_image = np.copy(image)
    i = 0
    colored_point = []
    for point in point_pixel_coords:
        x = point[0][0]
        y = point[0][1]
        if 0 <= y < result_image.shape[0] and 0 <= x < result_image.shape[1] and point_matrix[i,0]>=0 and point_matrix[i,0]<=5:
            point_colors_bgr[i] = image[y, x]
        i += 1
        if not i%500:
            print("Process now:%0.2f%%"%(i/num_points*100.0))
        # print(i/num_points*100.0)
    point_colors_rgb = point_colors_bgr[:, [2, 1, 0]]
    point_colors_rgb = point_colors_rgb / 255.0
    pcd.colors = o3d.utility.Vector3dVector(point_colors_rgb)
    o3d.visualization.draw_geometries([pcd])
    
    # Project to another picture
    pose_inverse = color_cloud.get_inverse_T(test_pose)
    pcd.transform(pose_inverse)
    # aft_img = color_cloud.color_pic(pcd,aft_pic_name,rvec,tvec,camera_intrinsic,distCoeffs)
    image = cv2.imread(aft_pic_name) # load the image
    points = np.asarray(pcd.points)
    num_points = points.shape[0]
    point_matrix = np.ones((num_points, 4))
    point_matrix[:, :3] = points  
    point_2d, _ = cv2.projectPoints(points, rvec, tvec, camera_intrinsic, distCoeffs)
    point_pixel_coords = point_2d.astype(int)

    result_image = np.copy(image)
    pcd_color = np.asarray(pcd.colors)[:, [2, 1, 0]]
    point_colors_bgr = np.zeros((point_pixel_coords.shape[0], 3), dtype=np.uint8)
    i = 0
    for point in point_pixel_coords:
        x = point[0][0]
        y = point[0][1]
        if 0 <= y < result_image.shape[0] and 0 <= x < result_image.shape[1] and point_matrix[i,0]>=0 and point_matrix[i,0]<=4.0:
            result_image[y, x] = pcd_color[i]*255.0
        i += 1
    cv2.imshow('Projected Points', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()