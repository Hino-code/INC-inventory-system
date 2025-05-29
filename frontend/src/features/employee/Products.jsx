import { useEffect, useState } from 'react';
import { getProducts } from '../../services/productAPI';
import ProductTable from '../../components/ProductTable';

export default function EmployeeProducts() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    const loadProducts = async () => {
      try {
        const res = await getProducts();
        setProducts(res);
      } catch (err) {
        console.error('Failed to load products:', err);
      }
    };
    loadProducts();
  }, []);

  return (
    <div className="container mt-4">
      <h4 className="mb-4">Product List</h4>
      <ProductTable data={products} />
    </div>
  );
}
