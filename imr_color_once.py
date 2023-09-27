import open3d as o3d
import numpy as np
import cv2 
import color_cloud
import copy

# Init the file name
pointcloud_file = 'data/pcds/0824.pcd'
img_file = 'F:/data/0814/pic_imr/pictures/1691140981.154829.jpg'
# key_frame = 'imr_txts/unique_sorted_key_frame.txt'
key_frame = 'result_frame.txt'

# Init the parameters
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
    # Load the files with given parameters
    pcd = o3d.io.read_point_cloud(pointcloud_file)
    points = np.asarray(pcd.points)
    num_points = points.shape[0]
    point_colors_bgr = np.ones((num_points, 3), dtype=np.uint8)
    pcd.colors = o3d.utility.Vector3dVector(point_colors_bgr)
    Trans, Stamps= color_cloud.key_frame_extract(key_frame)
    _,rvec,tvec = color_cloud.get_R_and_T(lidar_to_camera_extrinsic)

    # Load the pose info to matrix for loop
    pose = Trans[830]
    print(Stamps[830])
    pose_inverse = color_cloud.get_inverse_T(pose)
    pcd.transform(pose_inverse)
    
    # Choose function
    if_pic = False

    # Project pcd onto the image, project only once
    if if_pic:
        result = color_cloud.color_pic(pcd,img_file,rvec, tvec, camera_intrinsic, distCoeffs)
        cv2.imshow('Projected Points', result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    # Transform the color matrix from bgr to rgb so that pcd can be viewed normally
    else:
        point_colors_bgr = color_cloud.colorCloud(pcd,img_file,rvec, tvec, camera_intrinsic, distCoeffs,point_colors_bgr)
        point_colors_rgb = point_colors_bgr[:, [2, 1, 0]]
        point_colors_rgb = point_colors_rgb / 255.0
        pcd.transform(pose)
        pcd.colors = o3d.utility.Vector3dVector(point_colors_rgb)
        o3d.visualization.draw_geometries([pcd])
    o3d.io.write_point_cloud("data/result/copy_of_fragment.pcd", pcd)
    
    # # View coordinate of pointcloud
    # FOR1 = o3d.geometry.TriangleMesh.create_coordinate_frame(size=15, origin=[0, 0, 0])
    # pcd_T = copy.deepcopy(pcd)
    # pcd_T.transform(pose_inverse)
    # o3d.visualization.draw_geometries([FOR1,pcd_T], window_name="常规变换",
    #                           width=800,  # 窗口宽度
    #                           height=600)