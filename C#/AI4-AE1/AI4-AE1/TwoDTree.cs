using System;
using System.Collections;
using System.Collections.Generic;

namespace AI4_AE1
{
    class TwoDTree
    {
        private TwoDNode root;
        private int count;

        public int Count
        {
            get { return count; }
        }

        public TwoDTree()
        {
        }

        public void Insert(Point key, TwoDNode prev)
        {
            root = TwoDNode.insert(new Point(key), prev, root, 0);
        }

        public void InsertWithError(Point key, TwoDNode prev, double distance)
        {
            root = TwoDNode.insertWithError(new Point(key), prev, distance, root, 0);
        }

        public TwoDNode Search(Point key)
        {
            TwoDNode n = TwoDNode.search(key, root);

            return n;
        }

        public void Remove(Point key)
        {
            bool deleted = false;
            root = TwoDNode.remove(new Point(key), root, 0, ref deleted);
            if (deleted)
                count--;
        }

        public List<TwoDNode> Range(Point lowKey, Point upperKey)
        {

            List<TwoDNode> v = new List<TwoDNode>();
            TwoDNode.rsearch(new Point(lowKey), new Point(upperKey), root, 0, v);
            return v;
        }

        public TwoDNode Nearest(Point key)
        {
            return Nearest(key, 1)[0];
        }

        public TwoDNode[] Nearest(Point key, int n)
        {
            TwoDNode[] nbrs = new TwoDNode[n];
            NearestNeighborList nnl = new NearestNeighborList(n);

            Rect rect = Rect.inifiniteRect();
            double max_dist_sqd = Double.MaxValue;
            Point keyp = new Point(key);

            TwoDNode.nnbr(root, keyp, rect, max_dist_sqd, 0, nnl);

            for (int i = 0; i < n; ++i)
            {
                TwoDNode kd = (TwoDNode)nnl.removeHighest();
                nbrs[n - i - 1] = kd;
            }

            return nbrs;
        }

        private void preorder(TwoDNode node, List<TwoDNode> list)
        {
            list.Add(node);
            if (node.Left != null)
                preorder(node.Left, list);
            if (node.Right != null)
                preorder(node.Right, list);
        }

        private void inorder(TwoDNode node, List<TwoDNode> list)
        {
            if (node.Left != null)
                inorder(node.Left, list);
            list.Add(node);
            if (node.Right != null)
                inorder(node.Right, list);
        }

        public List<TwoDNode> Nodes()
        {
            List<TwoDNode> nodes = new List<TwoDNode>();
            if (root != null)
                inorder(root, nodes);
            return nodes;
        }
    }

    public class Rect
    {
        public Point min;
        public Point max;

        public Rect(Rect r)
        {
            this.min = new Point(r.min);
            this.max = new Point(r.max);
        }

        public Rect(Point min, Point max)
        {
            this.min = new Point(min);
            this.max = new Point(max);
        }

        public Point Closest(Point t)
        {
            Point p = new Point();

            if (t.X <= min.X)
                p.X = min.X;
            else if (t.X >= max.X)
                p.X = max.X;
            else
                p.X = t.X;

            if (t.Y <= min.Y)
                p.Y = min.Y;
            else if (t.X >= max.X)
                p.Y = max.Y;
            else
                p.Y = t.Y;

            return p;
        }

        public static Rect inifiniteRect()
        {
            Point min = new Point();
            Point max = new Point();

            min.X = Double.NegativeInfinity;
            min.Y = Double.NegativeInfinity;
            max.X = Double.PositiveInfinity;
            max.Y = Double.PositiveInfinity;

            return new Rect(min, max);
        }
    }

    class PriorityQueue
    {
        /**
         * The maximum priority possible in this priority queue.
         */
        private double maxPriority = Double.MaxValue;

        /**
         * This contains the list of objects in the queue.
         */
        private Object[] data;

        /**
         * This contains the list of prioritys in the queue.
         */
        private double[] value;

        /**
         * Holds the number of elements currently in the queue.
         */
        private int count;

        /**
         * This holds the number elements this queue can have.
         */
        private int capacity;

        /**
         * Creates a new <code>PriorityQueue</code> object. The
         * <code>PriorityQueue</code> object allows objects to be
         * entered into the queue and to leave in the order of
         * priority i.e the highest priority get's to leave first.
         */
        public PriorityQueue()
        {
            init(20);
        }

        /**
         * Creates a new <code>PriorityQueue</code> object. The
         * <code>PriorityQueue</code> object allows objects to
         * be entered into the queue an to leave in the order of
         * priority i.e the highest priority get's to leave first.
         *
         * @param capacity the initial capacity of the queue before
         * a resize
         */
        public PriorityQueue(int capacity)
        {
            init(capacity);
        }

        /**
         * Creates a new <code>PriorityQueue</code> object. The
         * <code>PriorityQueue</code> object allows objects to
         * be entered into the queue an to leave in the order of
         * priority i.e the highest priority get's to leave first.
         *
         * @param capacity the initial capacity of the queue before
         * a resize
         * @param maxPriority is the maximum possible priority for
         * an object
         */
        public PriorityQueue(int capacity, double maxPriority)
        {
            this.maxPriority = maxPriority;
            init(capacity);
        }

        /**
         * This is an initializer for the object. It basically initializes
         * an array of long called value to represent the prioritys of
         * the objects, it also creates an array of objects to be used
         * in parallel with the array of longs, to represent the objects
         * entered, these can be used to sequence the data.
         *
         * @param size the initial capacity of the queue, it can be
         * resized
         */
        private void init(int size)
        {
            capacity = size;
            data = new Object[capacity + 1];
            value = new double[capacity + 1];
            value[0] = maxPriority;
            data[0] = null;
        }

        /**
         * This function adds the given object into the <code>PriorityQueue</code>,
         * its priority is the long priority. The way in which priority can be
         * associated with the elements of the queue is by keeping the priority
         * and the elements array entrys parallel.
         *
         * @param element is the object that is to be entered into this
         * <code>PriorityQueue</code>
         * @param priority this is the priority that the object holds in the
         * <code>PriorityQueue</code>
         */
        public void add(Object element, double priority)
        {
            if (count++ >= capacity)
            {
                expandCapacity();
            }
            /* put this as the last element */
            value[count] = priority;
            data[count] = element;
            bubbleUp(count);
        }

        /**
         * Remove is a function to remove the element in the queue with the
         * maximum priority. Once the element is removed then it can never be
         * recovered from the queue with further calls. The lowest priority
         * object will leave last.
         *
         * @return the object with the highest priority or if it's empty
         * null
         */
        public Object remove()
        {
            if (count == 0)
                return null;
            Object element = data[1];
            /* swap the last element into the first */
            data[1] = data[count];
            value[1] = value[count];
            /* let the GC clean up */
            data[count] = null;
            value[count] = 0L;
            count--;
            bubbleDown(1);
            return element;
        }

        public Object front()
        {
            return data[1];
        }

        public double getMaxPriority()
        {
            return value[1];
        }

        /**
         * Bubble down is used to put the element at subscript 'pos' into
         * it's rightful place in the heap (i.e heap is another name
         * for <code>PriorityQueue</code>). If the priority of an element
         * at subscript 'pos' is less than it's children then it must
         * be put under one of these children, i.e the ones with the
         * maximum priority must come first.
         *
         * @param pos is the position within the arrays of the element
         * and priority
         */
        private void bubbleDown(int pos)
        {
            Object element = data[pos];
            double priority = value[pos];
            int child;
            /* hole is position '1' */
            for (; pos * 2 <= count; pos = child)
            {
                child = pos * 2;
                /* if 'child' equals 'count' then there
                   is only one leaf for this parent */
                if (child != count)

                    /* left_child > right_child */
                    if (value[child] < value[child + 1])
                        child++; /* choose the biggest child */
                /* percolate down the data at 'pos', one level
                   i.e biggest child becomes the parent */
                if (priority < value[child])
                {
                    value[pos] = value[child];
                    data[pos] = data[child];
                }
                else
                {
                    break;
                }
            }
            value[pos] = priority;
            data[pos] = element;
        }

        /**
         * Bubble up is used to place an element relatively low in the
         * queue to it's rightful place higher in the queue, but only
         * if it's priority allows it to do so, similar to bubbleDown
         * only in the other direction this swaps out its parents.
         *
         * @param pos the position in the arrays of the object
         * to be bubbled up
         */
        private void bubbleUp(int pos)
        {
            Object element = data[pos];
            double priority = value[pos];
            /* when the parent is not less than the child, end*/
            while (value[pos / 2] < priority)
            {
                /* overwrite the child with the parent */
                value[pos] = value[pos / 2];
                data[pos] = data[pos / 2];
                pos /= 2;
            }
            value[pos] = priority;
            data[pos] = element;
        }

        /**
         * This ensures that there is enough space to keep adding elements
         * to the priority queue. It is however advised to make the capacity
         * of the queue large enough so that this will not be used as it is
         * an expensive method. This will copy across from 0 as 'off' equals
         * 0 is contains some important data.
         */
        private void expandCapacity()
        {
            capacity = count * 2;
            Object[] elements = new Object[capacity + 1];
            double[] prioritys = new double[capacity + 1];
            Array.Copy(data, 0, elements, 0, data.Length);
            Array.Copy(value, 0, prioritys, 0, data.Length);
            data = elements;
            value = prioritys;
        }

        /**
         * This method will empty the queue. This also helps garbage
         * collection by releasing any reference it has to the elements
         * in the queue. This starts from offset 1 as off equals 0
         * for the elements array.
         */
        public void clear()
        {
            for (int i = 1; i < count; i++)
            {
                data[i] = null; /* help gc */
            }
            count = 0;
        }

        /**
         * The number of elements in the queue. The length
         * indicates the number of elements that are currently
         * in the queue.
         *
         * @return the number of elements in the queue
         */
        public int length()
        {
            return count;
        }
    }

    public class NearestNeighborList
    {
        public static int REMOVE_HIGHEST = 1;
        public static int REMOVE_LOWEST = 2;

        PriorityQueue m_Queue = null;
        int m_Capacity = 0;

        // constructor
        public NearestNeighborList(int capacity)
        {
            m_Capacity = capacity;
            m_Queue = new PriorityQueue(m_Capacity, Double.PositiveInfinity);
        }

        public double getMaxPriority()
        {
            if (m_Queue.length() == 0)
            {
                return Double.PositiveInfinity;
            }
            return m_Queue.getMaxPriority();
        }

        public bool insert(Object _object, double priority)
        {
            if (m_Queue.length() < m_Capacity)
            {
                // capacity not reached
                m_Queue.add(_object, priority);
                return true;
            }
            if (priority > m_Queue.getMaxPriority())
            {
                // do not insert - all elements in queue have lower priority
                return false;
            }
            // remove object with highest priority
            m_Queue.remove();
            // add new object
            m_Queue.add(_object, priority);
            return true;
        }

        public bool isCapacityReached()
        {
            return m_Queue.length() >= m_Capacity;
        }

        public Object getHighest()
        {
            return m_Queue.front();
        }

        public bool isEmpty()
        {
            return m_Queue.length() == 0;
        }

        public int getSize()
        {
            return m_Queue.length();
        }

        public Object removeHighest()
        {
            // remove object with highest priority
            return m_Queue.remove();
        }

    }

    public class TwoDNode
    {
        private Point key;
        //private Object value;
        private TwoDNode prev, next;
        private TwoDNode left, right;
        private bool deleted;

        private TwoDNode(Point key, TwoDNode prev)
        {
            this.key = key;
            this.prev = prev;
        }

        public Point Key
        {
            get { return key; }
        }

        public TwoDNode Previous
        {
            get { return prev; }
        }

        public TwoDNode Next
        {
            get { return next; }
        }

        public TwoDNode Left
        {
            get { return left; }
        }

        public TwoDNode Right
        {
            get { return right; }
        }

        public static TwoDNode insert(Point key, TwoDNode prev, TwoDNode tree, int level)
        {
            if (tree == null)
                tree = new TwoDNode(key, prev);
            else if (key == tree.key)
            {
                // Re-Insert
                if (tree.deleted)
                {
                    tree.deleted = false;
                    tree.prev = prev;
                }
                // Else duplicate key
            }
            else if ((level == 0 && key.X > tree.key.X) || (level == 1 && key.Y > tree.key.Y))
                tree.right = insert(key, prev, tree.right, (level + 1) % 2);
            else
                tree.left = insert(key, prev, tree.left, (level + 1) % 2);

            return tree;
        }

        public static TwoDNode insertWithError(Point key, TwoDNode prev, double allowedDistance, TwoDNode tree, int level)
        {
            if (tree == null)
                tree = new TwoDNode(key, prev);
            else if (key.Distance(tree.key) <= allowedDistance)
            {
                if (tree.deleted)
                {
                    tree.deleted = false;
                    tree.prev = prev;
                }
                // Else duplicate key
                // Check if the distance is longer then it might be the complete edge
                if (tree.prev != null && key.Distance(prev.key) > tree.key.Distance(tree.prev.key))
                    tree.prev = prev;
            }
            else if ((level == 0 && key.X > tree.key.X) || (level == 1 && key.Y > tree.key.Y))
                tree.right = insertWithError(key, prev, allowedDistance, tree.right, (level + 1) % 2);
            else
                tree.left = insertWithError(key, prev, allowedDistance, tree.left, (level + 1) % 2);

            return tree;
        }

        public static TwoDNode remove(Point key, TwoDNode tree, int level, ref bool deleted)
        {
            if (tree == null)
                return null;

            if (!tree.deleted && key == tree.key)
            {
                tree.deleted = true;
                deleted = true;
            }
            else if ((level == 0 && key.X > tree.key.X) || (level == 1 && key.Y > tree.key.Y))
                tree.right = remove(key, tree.right, (level + 1) % 2, ref deleted);
            else
                tree.left = remove(key, tree.left, (level + 1) % 2, ref deleted);

            if (!tree.deleted || tree.left != null || tree.right != null)
                return tree;
            else
                return null;
        }

        public static TwoDNode search(Point key, TwoDNode tree)
        {
            for (int level = 0; tree != null; level = (level + 1) % 2)
            {
                if (!tree.deleted && key == tree.key)
                    return tree;
                else if ((level == 0 && key.X > tree.key.X) || (level == 1 && key.Y > tree.key.Y))
                    tree = tree.right;
                else
                    tree = tree.left;
            }

            return null;
        }

#pragma warning disable 0642
        public static void rsearch(Point lowKey, Point upperKey, TwoDNode tree, int level, List<TwoDNode> v)
        {
            if (tree == null)
                return;

            if ((level == 0 && lowKey.X <= tree.key.X) || (level == 1 && lowKey.Y <= tree.key.Y))
                rsearch(lowKey, upperKey, tree.left, (level + 1) % 2, v);

            if (lowKey.X <= tree.key.X && upperKey.X >= tree.key.X)
                ;
            else if (lowKey.Y <= tree.key.Y && upperKey.Y >= tree.key.Y)
                ;
            else if (!tree.deleted)
                v.Add(tree);

            if ((level == 0 && upperKey.X > tree.key.X) || (level == 1 && upperKey.Y > tree.key.Y))
                rsearch(lowKey, upperKey, tree.right, (level + 1) % 2, v);
        }
#pragma warning restore 0642

        public static void nnbr(TwoDNode kd, Point target, Rect hr, double max_dist_sqd, int lev, NearestNeighborList nnl)
        {
            if (kd == null)
                return;

            int s = lev % 2;

            Point pivot = kd.key;
            double pivot_to_target = pivot.SquareDistance(target);

            Rect left_r = hr;
            Rect right_r = new Rect(hr);

            bool target_in_left;
            if (s == 0)
            {
                left_r.max.X = pivot.X;
                right_r.min.X = pivot.X;
                target_in_left = target.X < pivot.X;
            }
            else
            {
                left_r.max.Y = pivot.Y;
                right_r.min.Y = pivot.Y;
                target_in_left = target.Y < pivot.Y;
            }

            TwoDNode nearer_node;
            Rect nearer_rect;
            TwoDNode further_node;
            Rect further_rect;

            if (target_in_left)
            {
                nearer_node = kd.left;
                nearer_rect = left_r;
                further_node = kd.right;
                further_rect = right_r;
            }
            else
            {
                nearer_node = kd.right;
                nearer_rect = right_r;
                further_node = kd.left;
                further_rect = left_r;
            }

            nnbr(nearer_node, target, nearer_rect, max_dist_sqd, lev + 1, nnl);

            TwoDNode nearest = (TwoDNode)nnl.getHighest();
            double dist_sqd;

            if (!nnl.isCapacityReached())
                dist_sqd = Double.MaxValue;
            else
                dist_sqd = nnl.getMaxPriority();

            max_dist_sqd = Math.Min(max_dist_sqd, dist_sqd);

            Point closest = further_rect.Closest(target);
            if (closest.Distance(target) < Math.Sqrt(max_dist_sqd))
            {
                if (pivot_to_target < dist_sqd)
                {
                    nearest = kd;

                    dist_sqd = pivot_to_target;

                    if (!kd.deleted)
                        nnl.insert(kd, dist_sqd);

                    if (nnl.isCapacityReached())
                        max_dist_sqd = nnl.getMaxPriority();
                    else
                        max_dist_sqd = Double.MaxValue;
                }

                nnbr(further_node, target, further_rect, max_dist_sqd, lev + 1, nnl);
                TwoDNode temp_nearest = (TwoDNode)nnl.getHighest();
                double temp_dist_sqd = nnl.getMaxPriority();

                if (temp_dist_sqd < dist_sqd)
                {
                    nearest = temp_nearest;
                    dist_sqd = temp_dist_sqd;
                }
            }
            else if (pivot_to_target < max_dist_sqd)
            {
                nearest = kd;
                dist_sqd = pivot_to_target;
            }
        }

        public override string ToString()
        {
            return "TwoDTree";
            /*
            String s = String.Format("{0} {1}{2}", key, value, deleted ? "*" : "");
            if (left != null)
                s = String.Format("{0}\n L {1}", s, left.ToString());
            if (right != null)
                s = String.Format("{0}\n R {1}", s, right.ToString());

            return s;*/
        }
    }
}
