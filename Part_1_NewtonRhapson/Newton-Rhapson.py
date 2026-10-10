import numpy as np

def f(v):
    x, y = v[0], v[1]
    return x**4 + y**4 - 4*x*y + 1

def gradient(v):
    x,y = v[0], v[1]
    df_dx = 4*(x**3) - 4*y
    df_dy = 4*(y**3) - 4*x
    return np.array([df_dx, df_dy], dtype = float)

def hessian(v):
    x,y = v[0], v[1]
    df2_dx2 = 12*(x**2)
    df2_dy2 = 12*(y**2)
    df2_dxdy = -4
    df2_dydx = -4
    return np.array([[df2_dx2, df2_dxdy], [df2_dydx, df2_dy2]], dtype= float)

def newton_optimization(v0, tol=1e-6, max_iter=100):
    v = np.array(v0, dtype = float)

    for i in range(0, max_iter):
        g = gradient(v)
        h = hessian(v)
        norm_g = np.linalg.norm(g)

        if norm_g < tol:
            print(f'Hội tụ sau {i} lần lặp')
            print(f'Giá trị cực trị là: {f(v)}')
            print(f'Điểm cực trị là: {v}')
            return v
        try:
            delta_v = np.linalg.solve(h, -g)
        except np.linalg.LinAlgError:
            print('Ma trận Hessian bị suy biến')
            return None
        v = v + delta_v
    return v

if __name__ == '__main__':
    print('Phương trình f(x,y): x^4 + y^4 - 4xy + 1')
    x0 = float(input('Nhập tọa độ x0: '))
    y0 = float(input('Nhập tọa độ y0: '))
    vec = [x0, y0]
    vec_opt = newton_optimization(vec)