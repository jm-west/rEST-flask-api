from flask_restx import Namespace,Resource,fields
from flask_jwt_extended import jwt_required,get_jwt_identity
from ..models.orders import Order
from ..models.users import User
from http import HTTPStatus




orders_namespace = Namespace('orders', description='Orders operations')

order_model=orders_namespace.model(
    'Order',{
        'id':fields.Integer(description="An ID"),
        'size':fields.String(description="Size of order",required=True,
            enum=['SMALL','MEDIUM','LARGE','XLARGE']
        ),
        'status':fields.String(description="The status of the Order",
            required=True, enum=['PENDING','IN_TRANSIT','DELIVERED']
        )
    }
)


@orders_namespace.route('/order')

class OrderCreateGet(Resource):
    @orders_namespace.expect(order_model)
    @orders_namespace.marshal_with(order_model)
    # @jwt_required()
    def post(self):
        """
            place a new order
        """
        # username=get_jwt_identity()

        # current_user=User.query.filter_by(username=username).first()

        data=orders_namespace.payload


        new_order=Order(
            size=data['size'],
            quantity=data['quantity'],
            flavor=data['flavor'],
        )
        # new_order.users= current_user

        new_order.save()
        return new_order, HTTPStatus.CREATED
    
    @orders_namespace.marshal_with(order_model)
    @jwt_required()
    def get(self): #Gets all the orders
        """
        Gets all orders
        """
        orders = Order.query.all()
        return orders,HTTPStatus.OK

@orders_namespace.route('/order/<int:order_id>')
class GetUpdateDelete(Resource):
    def get(self,order_id):
        """
        Gets a single order
        """
        pass
    def post(self,order_id):
        """
        Updates a single order
        """
        pass
    def delete(self,order_id):
        """
        Deletes a single order
        """
        pass

@orders_namespace.route('/user/<int:user_id>/orders/<int:order_id>')
class GetSpecficOrderByUser(Resource):
    def get(self,user_id,order_id):
        """
        Gets a specific order by a user
        """
        pass

@orders_namespace.route('/user/<int:user_id>/orders')
class UserOrders(Resource):
    def get(self,user_id):
        """
        Gets all orders by a user
        """
        pass

@orders_namespace.route('/order/status/<int:order_id>')
class UpdatesOrderStatus(Resource):
    def patch(self,order_id):
        """
        Gets the status of an order
        """
        pass
