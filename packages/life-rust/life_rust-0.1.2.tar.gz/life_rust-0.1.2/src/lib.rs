use image::{ImageBuffer, Rgba};
use pyo3::prelude::*;

#[pyclass]
pub struct State {
    #[pyo3(get, set)]
    data: Vec<Vec<bool>>,
    #[pyo3(get, set)]
    size: (usize, usize),
}

impl Clone for State {
    fn clone(&self) -> Self {
        Self{ data: self.data.to_vec(),
        size: self.size}
    }
}

impl State {
    pub fn new(data: Vec<Vec<bool>>, size: (usize, usize)) -> Self {
        Self { data, size }
    }

    pub fn create_empty(n: usize, m: usize) -> Self {
        let v = vec![false; n];
        let v2 = vec![v; m];
        Self { data: v2, size: (n, m) }
    }

    pub fn neigh_count(&self, ix: usize, iy: usize) -> i32 {
        let mut count = 0;
        let x = ix; let y = iy;

        if y >= 1 {
            if x >= 1 && self.data[x-1][y-1] {count += 1};
            if self.data[x][y-1] {count += 1};
            if x+1 < self.size.1 && self.data[x+1][y-1] {count += 1};
        };

            if x >= 1 && self.data[x-1][y] {count += 1};
            if x+1 < self.size.1 && self.data[x+1][y] {count += 1};

        if y+1 < self.size.0 {
            if x >= 1 && self.data[x-1][y+1] {count += 1};
            if self.data[x][y+1] {count += 1};
            if x+1 < self.size.1 && self.data[x+1][y+1] {count += 1};
        };

        count
    }

    pub fn draw(&self, name: &str) {
        let x: u32 = self.size.0.try_into().unwrap();
        let y: u32 = self.size.1.try_into().unwrap();

        let mut buffer: ImageBuffer<Rgba<u8>, Vec<u8>> = ImageBuffer::from_pixel(x, y, Rgba([0, 0, 0, 30]));

        for (i, row) in self.data.iter().enumerate() {
            for (j, col) in row.iter().enumerate() {
                if *col {
                    let pos_y: u32 = i.try_into().unwrap();
                    let pos_x: u32 = j.try_into().unwrap();

                    buffer.get_pixel_mut(pos_x, pos_y).0 = [100, 255, 100, 255];
                }
            }
        }

        let x_resize: u32 = ( 256.0 * (x as f32 / y as f32) ).floor() as u32;
        let y_resize: u32 = ( 256.0 * (y as f32 / x as f32) ).floor() as u32;
        let resize = image::imageops::resize(&buffer, x_resize, y_resize, image::imageops::FilterType::Nearest);

        resize.save(name).unwrap();
    }

    pub fn next_tick(self) -> State {
        let mut new_matrix = State::create_empty(self.size.0, self.size.1);
        for (i, row) in self.data.iter().enumerate() {
            for (j, col) in row.iter().enumerate() {
                let neigh = self.neigh_count(i, j);
                if *col {
                    if neigh == 2 || neigh == 3 {
                        new_matrix.data[i][j] = true;
                    }
                } else {
                    if neigh == 3 {
                        new_matrix.data[i][j] = true;
                    }
                }
            }
        };

        new_matrix
    }
}

#[pyfunction]
fn generate(x:usize, y:usize, data: Vec<Vec<bool>>, id: &str) -> PyResult<State> {
    let state = State::new(data, (x, y));
    let filename: String = format!("{}.png", id);
    state.draw(&filename);
    Ok(state)
}

#[pyfunction]
fn next_tick(state: State, id: &str) -> PyResult<State> {
    let state = state.next_tick();
    let filename: String = format!("{}.png", id);
    state.draw(&filename);
    Ok(state)
}

#[pymodule]
#[pyo3(name = "life_rust")]
fn my_extension(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate, m)?)?;
    m.add_function(wrap_pyfunction!(next_tick, m)?)?;
    m.add_class::<State>()?;
    Ok(())
}