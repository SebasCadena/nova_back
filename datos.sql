--
-- PostgreSQL database dump
--

\restrict 96GffdGCSrlLeIdhiL43QBXcoqySsdWKcD68KgM3sIyeaGlK8BPKAbEbilIRxgv

-- Dumped from database version 16.11 (Ubuntu 16.11-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.11 (Ubuntu 16.11-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.users VALUES (1, 'Julian Ordóñez', 'julian@nova.com', 'hashed_password_123', 1, '2026-02-27 18:50:34.897');
INSERT INTO public.users VALUES (2, 'Maria Lopez', 'maria@gmail.com', 'hashed_password_456', 1, '2026-02-27 18:50:34.897');
INSERT INTO public.users VALUES (3, 'Carlos Perez', 'carlos@gmail.com', 'hashed_password_789', 1, '2026-02-27 18:50:34.897');


--
-- Data for Name: cart; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.cart VALUES (1, 1, '2026-02-27 18:50:47.92802', '2026-02-27 18:50:47.92802');
INSERT INTO public.cart VALUES (2, 2, '2026-02-27 18:50:47.92802', '2026-02-27 18:50:47.92802');


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.categories VALUES ('Audífonos', 'audifonos', '2026-02-19 12:28:10.842', '2026-02-19 12:28:10.842', 1);
INSERT INTO public.categories VALUES ('Cargadores', 'cargadores', '2026-02-19 12:28:10.842', '2026-02-19 12:28:10.842', 2);
INSERT INTO public.categories VALUES ('Power Banks', 'power-banks', '2026-02-19 12:28:10.842', '2026-02-19 12:28:10.842', 3);


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.products OVERRIDING SYSTEM VALUE VALUES ('UGREEN Nexode 140W GaN Charger', 'ugreen-nexode-140w-gan', 'Cargador USB-C 140W con tecnología GaN avanzada. Carga MacBook Pro 16 en 40 minutos. 2 puertos USB-C simultáneos. Compacto y premium.', 89.99, 'https://via.placeholder.com/500x500?text=UGREEN+140W+Charger', 2, true, '2026-02-19 12:29:45.323', '2026-02-19 12:29:45.323', 14, 10);
INSERT INTO public.products OVERRIDING SYSTEM VALUE VALUES ('UGREEN USB-C Hub 12 in 1', 'ugreen-usb-hub-12in1', 'Hub USB-C 12 puertos - 4K HDMI, USB 3.0, SD, Ethernet, PD 100W. Convierte tu laptop en workstation profesional. Compatible con MacBook y Windows.', 129.99, 'https://via.placeholder.com/500x500?text=USB-C+Hub+12in1', 2, true, '2026-02-19 12:29:45.323', '2026-02-19 12:29:45.323', 15, 10);
INSERT INTO public.products OVERRIDING SYSTEM VALUE VALUES ('UGREEN Lightning Cable 2M (3-pack)', 'ugreen-lightning-cable-3pack', 'Cables Lightning certificados MFi. 3 unidades de 2 metros. Carga y transferencia rápida. Durabilidad garantizada. Perfectos para oficina, hogar, carro.', 34.99, 'https://via.placeholder.com/500x500?text=Lightning+Cable+3Pack', 2, true, '2026-02-19 12:29:45.323', '2026-02-19 12:29:45.323', 16, 10);
INSERT INTO public.products OVERRIDING SYSTEM VALUE VALUES ('UGREEN 65W Car Charger Dual USB-C', 'ugreen-65w-car-charger-dual-usbc', 'Cargador para auto con 2 puertos USB-C y salida total 65W. Compatible con carga rápida PD y QC. Carga laptop y teléfono a la vez.', 29.99, 'https://via.placeholder.com/500x500?text=Car+Charger+65W', 2, true, '2026-02-19 12:29:45.323', '2026-02-19 12:29:45.323', 17, 10);
INSERT INTO public.products OVERRIDING SYSTEM VALUE VALUES ('UGREEN USB-C Cable 240W (2m)', 'ugreen-usbc-cable-240w-2m', 'Cable USB-C certificado para hasta 240W (PD 3.1). Ideal para laptops y estaciones de trabajo. Trenzado, resistente y confiable.', 19.99, 'https://via.placeholder.com/500x500?text=USB-C+Cable+240W', 2, true, '2026-02-19 12:29:45.323', '2026-02-19 12:29:45.323', 18, 10);
INSERT INTO public.products OVERRIDING SYSTEM VALUE VALUES ('UGREEN Power Bank 25000mAh 65W', 'ugreen-power-bank-25000', 'Power bank 25000mAh con carga rápida 65W. Carga tu iPhone 15 7 veces. USB-C entrada/salida. Display digital. Ultra rápido y confiable.', 79.99, 'https://via.placeholder.com/500x500?text=PowerBank+25000mAh', 3, true, '2026-02-19 12:29:45.323', '2026-02-19 12:29:45.323', 19, 10);
INSERT INTO public.products OVERRIDING SYSTEM VALUE VALUES ('UGREEN MagSafe Power Bank 10000mAh', 'ugreen-magsafe-power-bank-10000', 'Power bank magnético 10000mAh compatible con MagSafe. Carga inalámbrica 15W y USB-C 20W. Diseño compacto, ideal para iPhone y viajes.', 59.99, 'https://via.placeholder.com/500x500?text=MagSafe+PowerBank+10000', 3, true, '2026-02-19 12:29:45.323', '2026-02-19 12:29:45.323', 20, 10);
INSERT INTO public.products OVERRIDING SYSTEM VALUE VALUES ('UGREEN Power Bank 20000mAh 100W', 'ugreen-power-bank-20000-100w', 'Power bank 20000mAh con salida 100W y 2x USB-C. Carga MacBook, Steam Deck y más. Pantalla digital y múltiples protecciones.', 99.99, 'https://via.placeholder.com/500x500?text=PowerBank+20000mAh', 3, true, '2026-02-19 12:29:45.323', '2026-02-19 12:29:45.323', 21, 10);
INSERT INTO public.products OVERRIDING SYSTEM VALUE VALUES ('UGREEN Wireless Earbuds T8 Pro', 'ugreen-wireless-earbuds-t8', 'Audífonos inalámbricos con cancelación activa de ruido (ANC). Batería 10 horas. Conexión estable Bluetooth 5.3. Diseño ergonómico premium.', 199.99, 'https://via.placeholder.com/500x500?text=Earbuds+T8+Pro', 1, true, '2026-02-19 12:29:45.323', '2026-02-19 12:29:45.323', 22, 10);
INSERT INTO public.products OVERRIDING SYSTEM VALUE VALUES ('UGREEN AirLite ANC Headphones', 'ugreen-airlite-anc-headphones', 'Audífonos over-ear con ANC híbrido y 60 horas de batería. Sonido Hi-Res, modo transparencia y comodidad premium para largas jornadas.', 149.99, 'https://via.placeholder.com/500x500?text=AirLite+ANC+Headphones', 1, true, '2026-02-19 12:29:45.323', '2026-02-19 12:29:45.323', 23, 10);
INSERT INTO public.products OVERRIDING SYSTEM VALUE VALUES ('UGREEN Spark Buds Mini', 'ugreen-spark-buds-mini', 'Audífonos compactos con estuche ultraligero. Sonido balanceado, 30 horas con estuche y modo gaming de baja latencia.', 49.99, 'https://via.placeholder.com/500x500?text=Spark+Buds+Mini', 1, true, '2026-02-19 12:29:45.323', '2026-02-19 12:29:45.323', 24, 10);
INSERT INTO public.products OVERRIDING SYSTEM VALUE VALUES ('UGREEN Nexode 300W GaN Charger', 'ugreen-nexode-300w-gan', 'Cargador GaN de 300W con 6 puertos - el más potente del mercado. Carga 3 laptops simultáneamente. USB-C 140W, 2x USB-C 65W, 3x USB-A. Perfecto para profesionales.', 249.99, 'https://via.placeholder.com/500x500?text=UGREEN+300W+Charger', 2, true, '2026-02-19 12:29:45.323', '2026-02-19 12:29:45.323', 13, 10);
INSERT INTO public.products OVERRIDING SYSTEM VALUE VALUES ('Producto con stok', 'Stok.com', 'producto que contiene stok', 500, 'stok.jpeg', 2, true, '2026-02-23 09:25:40.289', '2026-02-23 09:25:40.289', 26, 3);


--
-- Data for Name: cart_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.cart_items VALUES (7, 1, 13, 2);
INSERT INTO public.cart_items VALUES (8, 1, 14, 1);
INSERT INTO public.cart_items VALUES (9, 2, 15, 1);


--
-- Data for Name: contact_messages; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.orders VALUES (1, 1, 'paid', 320000.00, '2026-02-27 18:54:58.920767');
INSERT INTO public.orders VALUES (2, 2, 'pending', 150000.00, '2026-02-27 18:54:58.920767');


--
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.order_items VALUES (4, 1, 13, 2, 120000.00);
INSERT INTO public.order_items VALUES (5, 1, 14, 1, 80000.00);
INSERT INTO public.order_items VALUES (6, 2, 15, 1, 150000.00);


--
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: services; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.services OVERRIDING SYSTEM VALUE VALUES ('Desarrollo de Páginas Web', 'desarrollo-paginas-web', 'Creamos sitios web modernos, responsivos y optimizados para SEO. Desde landing pages hasta portales corporativos completos con las últimas tecnologías.', 'globe', true, '2026-02-18 21:32:08.761', '2026-02-18 21:32:08.761', 11, 'Desde $500', 'Sitios web profesionales y optimizados para tu negocio', '["Diseño responsive", "Optimización SEO", "Panel de administración", "Integración con redes sociales", "Hosting y dominio incluido", "Mantenimiento mensual"]');
INSERT INTO public.services OVERRIDING SYSTEM VALUE VALUES ('Aplicaciones Móviles', 'aplicaciones-moviles', 'Desarrollamos apps nativas y multiplataforma para iOS y Android. Soluciones móviles que conectan tu negocio con tus clientes de manera directa y efectiva.', 'smartphone', true, '2026-02-18 21:32:08.761', '2026-02-18 21:32:08.761', 12, 'Desde $2,000', 'Apps móviles nativas y multiplataforma para tu empresa', '["Desarrollo iOS y Android", "Diseño UX/UI profesional", "Push notifications", "Integración con APIs", "Publicación en tiendas", "Soporte post-lanzamiento"]');
INSERT INTO public.services OVERRIDING SYSTEM VALUE VALUES ('Sistemas de Inventario', 'sistemas-inventario', 'Sistemas de gestión de inventario personalizados para optimizar el control de stock, productos y almacenes. Incluye reportes en tiempo real y alertas automáticas.', 'package', true, '2026-02-18 21:32:08.761', '2026-02-18 21:32:08.761', 13, 'Desde $1,500', 'Control total de tu inventario con reportes en tiempo real', '["Control de stock en tiempo real", "Gestión de múltiples almacenes", "Códigos de barras/QR", "Reportes y estadísticas", "Alertas de stock mínimo", "Integración con facturación"]');
INSERT INTO public.services OVERRIDING SYSTEM VALUE VALUES ('Modelos de Inteligencia Artificial', 'modelos-ia', 'Desarrollamos e implementamos modelos de IA personalizados: machine learning, análisis predictivo, chatbots inteligentes, reconocimiento de patrones y automatización con IA.', 'cpu', true, '2026-02-18 21:32:08.761', '2026-02-18 21:32:08.761', 14, 'Desde $3,000', 'Soluciones de IA para automatizar y optimizar tu negocio', '["Análisis predictivo", "Chatbots inteligentes", "Procesamiento de lenguaje natural", "Reconocimiento de imágenes", "Automatización de procesos", "Integración con sistemas existentes"]');
INSERT INTO public.services OVERRIDING SYSTEM VALUE VALUES ('Sistemas ERP Empresariales', 'sistemas-erp', 'Soluciones ERP completas para gestionar todos los procesos de tu empresa: ventas, compras, inventario, finanzas, recursos humanos y más, todo en una plataforma integrada.', 'building', true, '2026-02-18 21:32:08.761', '2026-02-18 21:32:08.761', 15, 'Desde $4,000', 'Sistema integral para gestionar toda tu empresa', '["Gestión de ventas y compras", "Control financiero", "Recursos humanos", "Reportes ejecutivos", "Facturación electrónica", "Multi-empresa y multi-moneda"]');
INSERT INTO public.services OVERRIDING SYSTEM VALUE VALUES ('E-commerce y Tiendas Online', 'ecommerce-tiendas', 'Tiendas online completas con carrito de compras, pasarelas de pago, gestión de productos y pedidos. Aumenta tus ventas llevando tu negocio al mundo digital.', 'shopping-cart', true, '2026-02-18 21:32:08.761', '2026-02-18 21:32:08.761', 16, 'Desde $1,800', 'Vende online con tu propia tienda virtual', '["Catálogo de productos ilimitado", "Múltiples métodos de pago", "Gestión de envíos", "Panel de administración", "Marketing y cupones", "Integración con redes sociales"]');
INSERT INTO public.services OVERRIDING SYSTEM VALUE VALUES ('Sistemas CRM', 'sistemas-crm', 'Software CRM para gestionar relaciones con clientes, seguimiento de ventas, automatización de marketing y análisis del embudo de conversión para aumentar tus ventas.', 'users', true, '2026-02-18 21:32:08.761', '2026-02-18 21:32:08.761', 17, 'Desde $2,500', 'Gestiona tus clientes y aumenta tus ventas', '["Gestión de contactos y leads", "Seguimiento de oportunidades", "Automatización de emails", "Reportes de ventas", "Pipeline visual", "Integración con WhatsApp"]');
INSERT INTO public.services OVERRIDING SYSTEM VALUE VALUES ('Aplicaciones Web Personalizadas', 'aplicaciones-web', 'Desarrollo de aplicaciones web a medida según las necesidades específicas de tu negocio. Sistemas complejos, portales, dashboards y más.', 'monitor', true, '2026-02-18 21:32:08.761', '2026-02-18 21:32:08.761', 18, 'Desde $2,000', 'Soluciones web a medida para necesidades específicas', '["Arquitectura escalable", "Múltiples usuarios y roles", "API REST integrada", "Seguridad avanzada", "Dashboards interactivos", "Integración con terceros"]');
INSERT INTO public.services OVERRIDING SYSTEM VALUE VALUES ('Automatización de Procesos', 'automatizacion-procesos', 'Automatizamos procesos repetitivos de tu empresa mediante scripts, integraciones y bots. Ahorra tiempo y reduce errores humanos con automatización inteligente.', 'zap', true, '2026-02-18 21:32:08.761', '2026-02-18 21:32:08.761', 19, 'Desde $1,000', 'Automatiza tareas repetitivas y ahorra tiempo', '["Integración entre sistemas", "Bots de automatización", "Procesamiento de documentos", "Notificaciones automáticas", "Reportes programados", "API personalizadas"]');
INSERT INTO public.services OVERRIDING SYSTEM VALUE VALUES ('Consultoría y Soporte Técnico', 'consultoria-soporte', 'Asesoría técnica especializada, auditoría de sistemas, optimización de infraestructura, soporte técnico continuo y capacitación para tu equipo.', 'headphones', true, '2026-02-18 21:32:08.761', '2026-02-18 21:32:08.761', 20, 'Desde $100/hora', 'Asesoría experta para tus proyectos tecnológicos', '["Auditoría de sistemas", "Optimización de performance", "Seguridad informática", "Migración de sistemas", "Capacitación de equipos", "Soporte técnico 24/7"]');


--
-- Name: cart_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cart_id_seq', 2, true);


--
-- Name: cart_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cart_items_id_seq', 9, true);


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categories_id_seq', 4, true);


--
-- Name: order_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.order_items_id_seq', 6, true);


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_id_seq', 2, true);


--
-- Name: payments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.payments_id_seq', 1, false);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.products_id_seq', 26, true);


--
-- Name: services_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.services_id_seq', 21, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 3, true);


--
-- PostgreSQL database dump complete
--

\unrestrict 96GffdGCSrlLeIdhiL43QBXcoqySsdWKcD68KgM3sIyeaGlK8BPKAbEbilIRxgv

