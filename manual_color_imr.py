import open3d as o3d
import numpy as np
import cv2 
import color_cloud

# Init the file name
pointcloud_file = 'data/pcds/0824.pcd'
img_files = ['data/pics/0.jpg',
             'data/pics/750.jpg',
             'data/pics/800.jpg',
             'data/pics/1000.jpg',
             'data/pics/1200.jpg',
             'data/pics/1280.jpg',
             'data/pics/1500.jpg']
# key_frame = 'data/key_frame.txt'
key_frame = 'result_frame.txt'
key_frame = 'E:/zyx/code/manual/key_frame.txt'

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
    Trans, Stamps= color_cloud.key_frame_extract(key_frame)
    _,rvec,tvec = color_cloud.get_R_and_T(lidar_to_camera_extrinsic)

    # Load the pose info to matrix for loop
    # poses = np.array([Trans[500],Trans[750],Trans[800],Trans[1000],
    #                   Trans[1200],Trans[1280],Trans[1500]])
    
    count = 0
    poses = []
    times = []
    img_files = []
    for pose in Trans:
        poses.append(Trans[count])
        times.append(float(Stamps[count]))
        count += 1
    
    Img_file = 'E:/zyx/code/manual/pic'
    img_list,img_name = color_cloud.get_img_list(Img_file)
    for time in times:
        filename = Img_file+'/'+color_cloud.get_img_name(img_list,img_name,time)
        img_files.append(filename)
        
    
    # Strat color process, color for one pose at a time
    count = 0.0
    print("Start Coloring")
    for pose,img_file in zip(poses,img_files):
        pose_inverse = color_cloud.get_inverse_T(pose)
        pcd.transform(pose_inverse)
        point_colors_bgr = color_cloud.colorCloud(pcd,img_file,rvec, tvec, camera_intrinsic, distCoeffs,point_colors_bgr)
        pcd.transform(pose)
        count += 1
        print("Current Process: %.2f%%" %(count/len(poses)*100.0),end='\r')
    print("\n Done, ready to plot")

    # Transform the color matrix from bgr to rgb so that pcd can be viewed normally
    point_colors_rgb = point_colors_bgr[:, [2, 1, 0]]
    point_colors_rgb = point_colors_rgb / 255.0
    pcd.colors = o3d.utility.Vector3dVector(point_colors_rgb)
    o3d.io.write_point_cloud("data/result/save.pcd", pcd)
    print("Saved")
    o3d.visualization.draw_geometries([pcd])
    
    